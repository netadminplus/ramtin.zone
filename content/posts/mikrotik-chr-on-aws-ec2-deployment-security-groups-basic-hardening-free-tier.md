---
title: "MikroTik CHR on AWS EC2: Deployment, Security Groups & Basic Hardening + FREE TIER 🚀"
date: 2026-02-10
slug: mikrotik-chr-on-aws-ec2-deployment-security-groups-basic-hardening-free-tier
categories: ["MikroTik", "Youtube Videos"]
youtube_id: 9Hwb0eI6x10
description: "In this MikroTik tutorial, I show you how to set up a MikroTik Cloud Server (CHR) on AWS (Amazon Web Services). AWS is the most powerful and reliable cloud provider in the world, and thanks to the AWS"
auto_generated: true
---
In this MikroTik tutorial, I show you how to set up a MikroTik Cloud Server (CHR) on AWS (Amazon Web Services). AWS is the most powerful and reliable cloud provider in the world, and thanks to the AWS Marketplace, we can easily deploy RouterOS on an EC2 instance. 🚀 Start with AWS Free Tier 👇 In this video, you will learn how to find the official MikroTik CHR image, launch it on an EC2 t3.micro instance, and configure it for free.

In this tutorial I walk through the whole setup step by step — what it is, what you need before you start, and the exact configuration that works. The video above shows the full lab; below is the written reference so you can follow along or copy the commands.

## What you will learn

- Introduction & Why MikroTik on AWS?
- Launching an EC2 Instance for MikroTik
- Finding the MikroTik CHR AMI in AWS Marketplace
- Instance Type (Free Tier Eligible), other settings & Launch the Instance
- Setting up Security Groups (Allowing Winbox & Services)
- Essential Router Hardening: Strong Passwords & Disabling unused Ports
- Activating CHR Trial License for Full Bandwidth
- Update MikroTik RouterOS
- Final Verification & Conclusion

## How it works

Kind: captions Language: en Hi everyone, I'm Ramin from Net Admin Hub. In this tutorial, I'm going to show you how to deploy a Micro cloud server on AWS. For example, you can set up your own VPN server or even you can connect your home and office networks together securely. In this video, I'll show you how to launch the instance, config your security group, and then we'll jump into Vimbox and close unnecessary ports and set a strong password on the Microix server. Here in AWS console from this menu you can see a wide range of services available in AWS but in this video we are going to use EC2 to create our cloud server inside AWS. If you use the EC2 uh service once you can see it under this recently visited uh box but also you can just search EC2 and open its console. Here you can see my EC2 console inside my AWS account. So click on launch and if I want to change my region for this server, I can just click here on Middle East for example I'm in this region and I can change it for example to North Virginia and create this cloud server in that specific location. In this page I need to fill some of these fields and create my server. Let's name it microick and for the image uh I need to click on this browse more AMIs and search for microick under this tab AWS marketplace AMIs. It's a specific image type provided by Microick to install routter OS on VMs and cloud server. And here you can see some information about MicroCHR inside AWS. And uh this image is selected for our cloud server. For the instance type, we need to select our resource.

You can see this T2 micro isn't available for this region. You can see T3 micro is available, two CPU cores, 1 GB of RAM and you can select uh the disk space here under this uh box. Uh you can see free tier eligible uh in front of this uh resource. Free tier is a type of service which Amazon provide. If you're new to AWS, you can use this free tier for a lot of its services. You can see here it allows us to use 750 hours per month for this uh free tier eligible uh EC2 machines. And you can see it allows us to send and receive uh 100 gigabyte traffic. And there are some more information here you can uh search and see. Uh this resource is selected and for key pair we actually don't need key pair for microick router OS. We can just create a new key pair but uh anyway we don't use it. Security group is basically a firewall between AWS and your cloud server. And we need to allow some traffic to access our microick. 1 GBTE of disk is good for me and click on launch instance. It says successfully initiated launch of this instance.

Here you can see some information about this machine. We can access this machine with uh IP address and also public DNS address. Here uh in this security tab, you can see our security group name is this one. We can click on this and allow some traffic to access this microick. Let me open a terminal and let me get back here to this page and copy this public IP address and open the terminal in my uh system. You can see uh it's not uh sending reply to us because this security uh policy doesn't allow it. And for security group we need to allow some traffic. You can see all outgoing traffic is allowed for this machine. So I can just click on edit inbound rule and add one rule. For example, if I want to access my win box, I can allow just for TCP uh 8291. Based on your security approach, you can just allow the desired traffic toward your cloud server. And this is a great security approach, but also you can allow all traffic toward your micro cloud server and handle the security in microick firewall level. But if I want to allow all traffic to this micro, I can use all traffic and the source will be anywhere IPv4. And for example, I set a comment which says allow all.

Just another note here, uh you don't have to allow anything from anywhere to your server. Based on your project and your use case, you can add your particular IP addresses here and allow access to this server for just that specified IP addresses. If I save this rule, you can see now I can ping this machine here. You can see we're getting reply and we need to immediately log this routter so we can change its password. Let's open Winimbox and let me open it in this window so you can see it too. And the pass the user is admin and it doesn't have any password by default. We are logged into our microick CHR and here in IP and then services I need to disable all unnecessary services for example API API SSL FTP SSH TNET we don't need them uh let's change the Windbox port let's change it to 80 to 92 and for the HTTP port I'll use 8080 for example and set uh a strong password for admin user is crucial. System users and let's set a strong password for this user and it's done. As you know CHR uh by default provides us a free license which limits us to 1 mgabits of bandwidth. So here in system and then license let me find it here. If you have a account in micro website which is completely free, you can renew your license by entering your account information. My username is this one and I enter my password of my account and the level uh I select P unlimited for unlimited bandwidth on my network interface. Let's click on start and you can see my level is upgraded and now here in system and then resources you can see my router OS version is 7.1 and I can upgrade it. System and then packages and uh check for update the latest version available is 7.21.2 and I want to download and install it.

## Wrapping up

If this helped, subscribe to Ramtin Tech Zone on YouTube for more MikroTik, Linux, networking, VPN and AI tutorials — and if a script or tutorial saved you time, consider supporting the work on the Donate page.
