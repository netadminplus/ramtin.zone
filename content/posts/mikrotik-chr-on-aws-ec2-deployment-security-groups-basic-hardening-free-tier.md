---
title: "MikroTik CHR on AWS EC2: Deployment, Security Groups & Basic Hardening + FREE TIER 🚀"
date: 2026-02-10
slug: mikrotik-chr-on-aws-ec2-deployment-security-groups-basic-hardening-free-tier
categories: ["MikroTik", "Youtube Videos"]
youtube_id: 9Hwb0eI6x10
description: "In this MikroTik tutorial, I show you how to set up a MikroTik Cloud Server (CHR) on AWS (Amazon Web Services). AWS is the most powerful and reliable cloud provider in the world, and thanks to the AWS Marketplace, we can easily deploy RouterOS on an EC2 instance."
---

A MikroTik in the cloud is one of those things that sounds complicated until you actually do it. Once it is running, it opens up a lot: your own VPN server, a core router for cloud infrastructure, or a secure link between your home and office networks.

AWS makes the deployment part easy, because the official MikroTik CHR image is right there in the AWS Marketplace. The part that needs care is what happens after the instance boots. A fresh CHR has no password, and it sits on a public IP. So the first login and the first hardening steps matter more than the launch itself.

In this lab, I deploy a MikroTik CHR on AWS EC2:

- Find the official CHR image in the AWS Marketplace and launch it on a free-tier-eligible instance
- Set up the security group so only the traffic I want reaches the router
- Log in with WinBox, set a strong password, and close the services I do not need
- Activate the CHR trial license to remove the 1 Mbps free-license limit
- Update RouterOS to the latest version and verify the result

## What We're Building

CHR stands for Cloud Hosted Router. It is a version of RouterOS built to run as a virtual machine, and MikroTik ships it as a ready-made image for cloud platforms.

On AWS, the setup is an EC2 instance running that CHR image. AWS controls what reaches the instance through a security group, and RouterOS controls what happens inside it. Both layers need attention, and in that order: the security group first, then the router itself.

## Before You Start

You need an AWS account and access to the EC2 console. Pick your region before you launch. I was in the Middle East region in the video, and the region picker sits at the top of the console. The region decides where the server physically runs and which instance types are available there.

You also need a free MikroTik account. The trial license step uses it, and all CHR license management runs through the MikroTik account system.

## Step 1: Launch the EC2 Instance

In the EC2 console, click Launch instance and name it. I named mine `mikrotik`.

For the image, click Browse more AMIs, open the AWS Marketplace AMIs tab, and search for MikroTik. The CHR image appears there. The Marketplace page listed 7.15.1 as the latest version at the time. Click Subscribe, and the image is selected for the instance.

Next comes the instance type. The t2.micro was not available in my region, so I picked the t3.micro instead: two CPU cores and 1 GB of RAM. It showed as free tier eligible. When I checked the limits on the AWS page that day, the EC2 free tier allowed 750 hours a month of eligible instance usage and 100 GB of traffic.

For the key pair, pick Proceed without a key pair. RouterOS does not use an AWS key pair, so there is nothing to gain from creating one here.

Set the disk size, then click Launch instance. The console reports that the launch started, and a few moments later the instance is up and running. The instance page shows the public IP address and the public DNS name. Both work for reaching the router.

## Step 2: Set Up the Security Group

A security group is a firewall between AWS and your server. The default group the launch created allowed SSH, HTTPS, and HTTP. That is a starting point, not a finished configuration.

A security group has two parts. The outbound rules were fine: all outgoing traffic is allowed. The inbound rules are the part that matters. Before I changed anything, I pinged the public IP from my own terminal and got no reply. The security group was blocking it.

Click the security group, then Edit inbound rules, and add a rule for the traffic you actually need. To reach WinBox, that is TCP port 8291. Save the rule, and the ping starts getting replies.

There is a second way to do this, and I want to be honest about the trade-off. You can allow all traffic from anywhere and handle the security at the RouterOS firewall level instead. That works, but I recommend allowing only the traffic you need. If your project allows it, restrict the source to your own IP addresses instead of anywhere. A cloud router with an open management port and a weak password will not stay yours for long.

## Step 3: First Login and Basic Hardening

Open WinBox and connect to the public IP. The username is `admin`, and there is no password by default. Log in and change that immediately.

Go to IP, then Services, and disable the services you do not need: API, API-SSL, FTP, SSH, and Telnet. Then change the ports on the services you keep. I moved the WinBox port to 8292 and the HTTP port to 8080.

Then go to System, then Users, and set a strong password for the admin user. Do this in the same session as the first login. A fresh CHR on a public IP with the default login is an open door, and the window between launch and hardening should be minutes, not hours.

Expected result after this step: WinBox connects on the new port with the new password, and the services list shows only WinBox and WebFig still running.

## Step 4: Activate the Trial License

A fresh CHR runs on the free license, which limits each interface to 1 Mbps. That is fine for a test, but not for real use.

Go to System, then License. The level shows as free. Click Renew License, enter your MikroTik account username and password, and select P-Unlimited as the level. The license upgrades, and the 1 Mbps limit is gone.

The trial is free for 60 days and covers any of the paid license levels. P-Unlimited is the top level, with no enforced speed limit, so the CHR runs at whatever the network card and the instance can deliver.

## Step 5: Update RouterOS and Verify

With the license sorted, check the version. System, then Resources, shows the version the AMI shipped with. Then go to System, then Packages, and Check for Updates. The latest version offered was 7.21.2. Download and install it, and the router reboots.

Log back in with the new WinBox port and the new password, and check System, then Resources again. The version now shows the update installed.

Expected result: the CHR is up and running on AWS, reachable on the hardened ports, licensed for full bandwidth, and running the latest RouterOS.

## One Limitation to Keep in Mind

The hardening in this video is basic setup only. It covers the first login, the password, the unused services, and the ports. That is the minimum a cloud router needs on day one, and it is not a production hardening guide.

For a production server, you need real firewall rules on the router itself, not just the security group. If you want a dedicated video on professional MikroTik hardening, that is a separate topic, and it deserves its own lab.

## Final Thoughts

Deploying CHR on AWS is mostly a Marketplace exercise. The image is official, the t3.micro fits the free tier, and the launch takes a few minutes. The real work is the ten minutes after the launch: the security group, the password, the services, and the license.

Get those four right and the cloud router is a solid box to build on, whether it ends up as a VPN server or the link between two offices. Skip them, and the free tier price does not matter, because the router will not be yours for long.

## Official Documentation

- [CHR Licensing — MikroTik Manual](https://manual.mikrotik.com/docs/getting-started/routeros-licensing/chr/chr-licensing/)
- [AWS Free Tier](https://aws.amazon.com/free/)
