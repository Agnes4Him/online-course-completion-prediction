resource "aws_vpc" "model_vpc" {
  cidr_block = var.vpc_cidr

  tags = {
    Name = var.vpc_tag
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.model_vpc.id

  tags = {
    Name = "igw"
  }
}

resource "aws_subnet" "private_subnetA" {
  vpc_id            = aws_vpc.model_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"

  tags = {
    "Name"                            = "PrivateSubnetA"
    "kubernetes.io/role/internal-elb" = "1"
    "kubernetes.io/cluster/model"      = "owned"
  }
}

resource "aws_subnet" "private_subnetB" {
  vpc_id            = aws_vpc.model_vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1b"

  tags = {
    "Name"                            = "PrivateSubnetB"
    "kubernetes.io/role/internal-elb" = "1"
    "kubernetes.io/cluster/model"      = "owned"
  }
}

resource "aws_subnet" "public_subnetA" {
  vpc_id                  = aws_vpc.model_vpc.id
  cidr_block              = "10.0.3.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    "Name"                       = "PublicSubnetA"
    "kubernetes.io/role/elb"     = "1"
    "kubernetes.io/cluster/model" = "owned"
  }
}

resource "aws_subnet" "public_subnetB" {
  vpc_id                  = aws_vpc.model_vpc.id
  cidr_block              = "10.0.4.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true

  tags = {
    "Name"                       = "PublicSubnetB"
    "kubernetes.io/role/elb"     = "1"
    "kubernetes.io/cluster/model" = "owned"
  }
}

resource "aws_subnet" "db_subnetA" {
  vpc_id                  = aws_vpc.model_vpc.id
  cidr_block              = "10.0.5.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true

  tags = {
    "Name"                = "DBSubnetA"
  }
}

resource "aws_subnet" "db_subnetB" {
  vpc_id                  = aws_vpc.model_vpc.id
  cidr_block              = "10.0.6.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true

  tags = {
    "Name"                = "DBSubnetB"
  }
}

resource "aws_eip" "nat" {
  domain = "vpc"

  tags = {
    Name = "NAT"
  }
}

resource "aws_nat_gateway" "nat_gw" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public_subnetA.id

  tags = {
    Name = "NATgw"
  }

  depends_on = [aws_internet_gateway.igw]
}

resource "aws_route_table" "private_RT" {
  vpc_id = aws_vpc.model_vpc.id

  route {
    cidr_block                 = "0.0.0.0/0"
    nat_gateway_id             = aws_nat_gateway.nat_gw.id
  }

  tags = {
    Name = "PrivateRT"
  }
}

resource "aws_route_table" "public_RT" {
  vpc_id = aws_vpc.model_vpc.id

  route {
    cidr_block                 = "0.0.0.0/0"
    gateway_id                 = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "PublicRT"
  }
}

resource "aws_route_table_association" "private_RT_associationA" {
  subnet_id      = aws_subnet.private_subnetA.id
  route_table_id = aws_route_table.private_RT.id
}

resource "aws_route_table_association" "private_RT_associationB" {
  subnet_id      = aws_subnet.private_subnetB.id
  route_table_id = aws_route_table.private_RT.id
}

resource "aws_route_table_association" "public_RT_associationA" {
  subnet_id      = aws_subnet.public_subnetA.id
  route_table_id = aws_route_table.public_RT.id
}

resource "aws_route_table_association" "public_RT_associationB" {
  subnet_id      = aws_subnet.public_subnetB.id
  route_table_id = aws_route_table.public_RT.id
}

output "vpc_id" {
  value = aws_vpc.model_vpc.id
}

output "db_subnetA" {
  value = aws_subnet.db_subnetA.id
}

output "db_subnetB" {
  value = aws_subnet.db_subnetB.id
}