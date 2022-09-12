"""The module contains implementation of the MLFlow tracking servers deployed on AWS."""

from aws_cdk import App, Aws, CfnOutput, CfnParameter, Duration, RemovalPolicy, Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import aws_iam as iam
from aws_cdk import aws_rds as rds
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_secretsmanager as sm
from constructs import Construct


class DeploymentStack(Stack):
    """AWS stack to be deployed.

    Args:
            scope: Scope of the deploying stack.
            idx: Name of the deploying stack.
            **kwargs: Any additional key-word arguments that will be passed to Stack.__init__.
    """

    # pylint: disable=too-many-locals
    def __init__(self, scope: Construct, idx: str, **kwargs) -> None:
        super().__init__(scope, idx, **kwargs)
        # ==============================
        # ======= CFN PARAMETERS =======
        # ==============================
        project_name_param = CfnParameter(scope=self, id="ProjectName", type="String")
        db_name = "mlopszoomcampdb"
        port = 3306
        username = "master"
        bucket_name = f"{project_name_param.value_as_string}-artifacts-{Aws.ACCOUNT_ID}"
        container_repo_name = "mlops-zoomcamp-containers"  # pylint: disable=unused-variable
        cluster_name = "mlops-zoomcamp"
        service_name_mlflow = "mlflow"
        service_name_prefect = "prefect"

        # ==================================================
        # ================= IAM ROLE =======================
        # ==================================================
        role = iam.Role(
            scope=self,
            id="TASKROLE",
            assumed_by=iam.ServicePrincipal(service="ecs-tasks.amazonaws.com"),
        )
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
        )
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonECS_FullAccess")
        )

        # ==================================================
        # ================== SECRET ========================
        # ==================================================
        db_password_secret = sm.Secret(
            scope=self,
            id="DBSECRET",
            secret_name="dbPassword",
            generate_secret_string=sm.SecretStringGenerator(
                password_length=20, exclude_punctuation=True
            ),
        )

        # ==================================================
        # ==================== VPC =========================
        # ==================================================
        public_subnet = ec2.SubnetConfiguration(
            name="Public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=28
        )
        private_subnet = ec2.SubnetConfiguration(
            name="Private", subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT, cidr_mask=28
        )
        isolated_subnet = ec2.SubnetConfiguration(
            name="DB", subnet_type=ec2.SubnetType.PRIVATE_ISOLATED, cidr_mask=28
        )

        vpc = ec2.Vpc(
            scope=self,
            id="VPC",
            cidr="10.0.0.0/24",
            max_azs=2,
            nat_gateway_provider=ec2.NatProvider.gateway(),
            nat_gateways=1,
            subnet_configuration=[public_subnet, private_subnet, isolated_subnet],
        )
        vpc.add_gateway_endpoint("S3Endpoint", service=ec2.GatewayVpcEndpointAwsService.S3)
        # ==================================================
        # ================= S3 BUCKET ======================
        # ==================================================
        artifact_bucket = s3.Bucket(
            scope=self,
            id="ARTIFACTBUCKET",
            bucket_name=bucket_name,
            public_read_access=False,
            removal_policy=RemovalPolicy.DESTROY,
        )
        # # ==================================================
        # # ================== DATABASE  =====================
        # # ==================================================
        # Creates a security group for AWS RDS
        sg_rds = ec2.SecurityGroup(scope=self, id="SGRDS", vpc=vpc, security_group_name="sg_rds")
        # Adds an ingress rule which allows resources in the VPC's CIDR to access the database.
        sg_rds.add_ingress_rule(peer=ec2.Peer.ipv4("10.0.0.0/24"), connection=ec2.Port.tcp(port))

        database = rds.DatabaseInstance(
            scope=self,
            id="POSTGRES",
            database_name=db_name,
            port=port,
            credentials=rds.Credentials.from_username(
                username=username, password=db_password_secret.secret_value
            ),
            engine=rds.DatabaseInstanceEngine.postgres(version=rds.PostgresEngineVersion.VER_14_3),
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO),
            vpc=vpc,
            security_groups=[sg_rds],
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED),
            # multi_az=True,
            removal_policy=RemovalPolicy.DESTROY,
            deletion_protection=False,
        )

        # ==================================================
        # ============== TASK DEFINITIONS ==================
        # ==================================================
        task_definition_mlflow = ecs.FargateTaskDefinition(
            scope=self,
            id="MLflow",
            task_role=role,
        )

        task_definition_prefect = ecs.FargateTaskDefinition(
            scope=self,
            id="Prefect",
            task_role=role,
        )

        # ==================================================
        # ======== FARGATE SERVICE ==================
        # ==================================================
        cluster = ecs.Cluster(scope=self, id="CLUSTER", cluster_name=cluster_name, vpc=vpc)

        fargate_service_mlflow = ecs_patterns.NetworkLoadBalancedFargateService(
            scope=self,
            id="MLFLOW",
            service_name=service_name_mlflow,
            cluster=cluster,
            task_definition=task_definition_mlflow,
        )

        fargate_service_prefect = ecs_patterns.NetworkLoadBalancedFargateService(
            scope=self,
            id="PREFECT",
            service_name=service_name_prefect,
            cluster=cluster,
            task_definition=task_definition_prefect,
        )

        # Setup security group
        fargate_service_mlflow.service.connections.security_groups[0].add_ingress_rule(
            peer=ec2.Peer.ipv4(vpc.vpc_cidr_block),
            connection=ec2.Port.tcp(5000),
            description="Allow inbound from VPC for mlflow",
        )

        fargate_service_prefect.service.connections.security_groups[0].add_ingress_rule(
            peer=ec2.Peer.ipv4(vpc.vpc_cidr_block),
            connection=ec2.Port.tcp(4200),
            description="Allow inbound from VPC for Prefect",
        )

        # Setup autoscaling policy
        scaling_mlflow = setup_autoscaling(fargate_service_mlflow)
        scaling_prefect = setup_autoscaling(fargate_service_prefect)
        # ==================================================
        # =================== OUTPUTS ======================
        # ==================================================
        CfnOutput(
            scope=self,
            id="MLFlowLoadBalancerDNS",
            value=fargate_service_mlflow.load_balancer.load_balancer_dns_name,
        )
        CfnOutput(
            scope=self,
            id="PrefectLoadBalancerDNS",
            value=fargate_service_prefect.load_balancer.load_balancer_dns_name,
        )
        CfnOutput(scope=self, id="MLFlowArtifactBucketName", value=artifact_bucket.bucket_name)

        # ==================================================
        # ============== MLFLOW CONTAINER ==================
        # ==================================================

        mlflow_port = 5000

        container_mlflow = task_definition_mlflow.add_container(
            id="Mlflow_Container",
            image=ecs.ContainerImage.from_asset(directory="mlflow_container"),
            environment={
                "BUCKET": f"s3://{artifact_bucket.bucket_name}",
                "HOST": database.db_instance_endpoint_address,
                "PORT": str(port),
                "DATABASE": db_name,
                "USERNAME": username,
                "MLFLOW_PORT": mlflow_port,
            },
            secrets={"PASSWORD": ecs.Secret.from_secrets_manager(db_password_secret)},
            logging=ecs.LogDriver.aws_logs(stream_prefix="mlflow"),
        )
        port_mapping = ecs.PortMapping(
            container_port=mlflow_port, host_port=mlflow_port, protocol=ecs.Protocol.TCP
        )
        container_mlflow.add_port_mappings(port_mapping)

        # ==================================================
        # ============= PREFECT CONTAINER ==================
        # ==================================================
        prefect_port = 4200

        container_prefect = task_definition_prefect.add_container(
            id="Prefect_Container",
            image=ecs.ContainerImage.from_asset(directory="prefect_container"),
            logging=ecs.LogDriver.aws_logs(stream_prefix="prefect"),
            environment={
                "PREFECT_PORT": prefect_port,
                "EXTERNAL_URL": fargate_service_prefect.load_balancer.load_balancer_dns_name,
            },
        )
        port_mapping = ecs.PortMapping(
            container_port=prefect_port, host_port=prefect_port, protocol=ecs.Protocol.TCP
        )
        container_prefect.add_port_mappings(port_mapping)


def setup_autoscaling(
    fargate_service: ecs_patterns.NetworkLoadBalancedFargateService, max_capacity: int = 1
):
    scaling = fargate_service.service.auto_scale_task_count(max_capacity=max_capacity)
    scaling.scale_on_cpu_utilization(
        id="AUTOSCALING",
        target_utilization_percent=70,
        scale_in_cooldown=Duration.seconds(60),
        scale_out_cooldown=Duration.seconds(60),
    )
    return scaling


app = App()
DeploymentStack(app, "DeploymentStack")
app.synth()
