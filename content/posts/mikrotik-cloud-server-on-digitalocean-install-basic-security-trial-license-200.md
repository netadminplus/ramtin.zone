---
title: "MikroTik Cloud Server on DigitalOcean: Install, Basic Security & Trial License + $200 FREE CREDIT 🔥"
date: 2026-01-19
slug: mikrotik-cloud-server-on-digitalocean-install-basic-security-trial-license-200
categories: ["MikroTik", "Youtube Videos"]
youtube_id: D9q2OqkFHtk
description: "In this MikroTik tutorial, I show you how to set up a MikroTik Cloud Server on DigitalOcean. DigitalOcean is a high-quality and affordable cloud provider, but they don’t offer RouterOS in their default OS list."
---

DigitalOcean is a solid, affordable cloud provider, but it does not offer RouterOS in its default OS list. So if you want a MikroTik in the cloud on DigitalOcean, you install it yourself with a custom image.

That sounds like extra work, and it is one extra step. But the whole setup still takes a few minutes, and the result is a $4-a-month cloud router you can use as a VPN server or as the link between your networks.

In this lab, I install MikroTik CHR on DigitalOcean:

- Download the CHR raw disk image from MikroTik and upload it as a custom image
- Create a $4 droplet with the smallest resources
- Log in right away, set a strong password, and close the services I do not need
- Create a new full-access user and delete the default admin account
- Activate the CHR trial license to remove the 1 Mbps free-license limit
- Verify connectivity and look at the default configuration

## What We're Building

The plan is simple. DigitalOcean runs a droplet from a disk image we supply. That image is the official MikroTik CHR image, so the droplet boots straight into RouterOS.

The one thing to understand before starting: the moment this droplet gets a public IP, it is reachable from the whole internet, with a known default login. The hardening steps are not a finishing touch. They are the first thing to do after the droplet boots.

## Before You Start

You need a DigitalOcean account. Signing up is free, and the referral link in the video description gives $200 of free credit for 60 days.

You also need a free MikroTik account for the trial license step. And you need an SSH key added to your DigitalOcean account, because DigitalOcean asks for an authentication method when you create the droplet, and I selected SSH key.

## Step 1: Download the CHR Image

Open the MikroTik website, go to the download section, and open the CHR tab. MikroTik had just released 7.20.7 in the long-term channel, and that is the version I downloaded. Take the raw disk image.

Extract the zip file. The file you need has the `.img` extension.

## Step 2: Upload It as a Custom Image

In DigitalOcean, create a droplet. On the OS selection page, there are three tabs. The first is the regular OS list, the second is the Marketplace, and the third is Custom Images. RouterOS is not in the first two, so open Custom Images and click Add image.

You get two options: upload from a direct link, or upload from your own system. I uploaded the `.img` file from my system.

Give the image a name. I used `mikrotik-7.20.7`. For the distribution, I selected Unknown; that field does not matter much here. Select the region the image should be uploaded to. I picked Frankfurt. Add a tag and a note if you want, then upload, and wait for it to finish.

Expected result: the custom image appears in your image list, ready to use for a droplet.

## Step 3: Create the Droplet

Create another droplet. Select the region first. I stayed with Frankfurt. The New York region shows three data centers in the list, so regions can have more than one location.

For the OS, the custom image is already selected. For resources, MikroTik does not need much. I took the smallest regular option: 512 MB of RAM, one CPU core, 10 GB of disk, and 500 GB of data transfer a month. It costs $4 a month.

Skip the additional storage and the backup option. I run a script on the router that takes a daily backup and sends it by email or Telegram, so I do not pay DigitalOcean for backups.

For authentication, select SSH key. RouterOS has no root account, so this is the method I used. Set the hostname. I named it `mikrotik-test`. Then click Create Droplet. After a few seconds, the server is ready.

## Step 4: Harden It Immediately

This is the step that matters most. Copy the droplet IP, open WinBox, and log in. The user is `admin`, and there is no password by default.

First, set a password. Go to System, then Password, and set a strong one.

Then go to IP, then Services, and disable the services you do not need: API, API-SSL, FTP, SSH, and Telnet. Keep WinBox and WebFig, but change their ports. I moved the WinBox port to 8292 and the HTTP port to 8080.

Next, create a new user with full access. Go to System, then Users, and add a user. I named mine `ramtin`, set the group to full, and set a complex password. Then disconnect, log back in with the new user, and delete the admin account.

I say this plainly because it is the whole point of the step: if you skip the hardening, a fresh MikroTik on a public IP usually gets attacked within seconds. The password, the closed services, and the deleted admin account are the minimum.

Expected result: the only way in is the new user on the new WinBox port, and the services list shows only WinBox and WebFig.

## Step 5: Activate the Trial License

The free CHR license limits each interface to 1 Mbps. That is far below what the droplet can do, so the license needs an upgrade.

Go to System, then License. The level shows as free. MikroTik CHR has four license levels, and the trial lets you test any of the paid levels free for 60 days with a MikroTik account.

Click Renew License, enter your MikroTik account email and password, and select P-Unlimited as the level. P-Unlimited has no speed limit, so the CHR runs at whatever the droplet network card provides.

One honest detail from the lab: my first attempt failed with a wrong-password error. I checked the password again, tried once more, and it went through. The license level then showed P-Unlimited.

## Step 6: Verify It Works

Open a terminal on the router and ping the Cloudflare DNS address. I got replies at about 1 millisecond. Then ping msn.com. That worked too, so the router has internet access.

Then run `/export` to look at the default configuration. The only configuration on the server is the DHCP client on ether1. In Interfaces, the droplet has two network interfaces by default, and in IP, then Addresses, the public IP sits on ether1.

Expected result: the CHR is up, licensed for full bandwidth, hardened at the basic level, and passing traffic.

## One Limitation to Keep in Mind

This is a basic setup, and it is not enough for a production server. The password, the closed services, and the new user cover the first day. A production router needs real firewall rules on top of this.

If you want a dedicated video on professional MikroTik hardening, that is a separate lab, and it deserves the full treatment.

## Final Thoughts

DigitalOcean does not hand you RouterOS, but the custom image path is short: download the raw image, upload it, pick the $4 droplet, and boot. The install is the easy part.

The part that decides whether the setup survives is the five minutes after boot. Set the password, close the services, replace the admin account, and activate the trial license. Do that, and a $4 droplet becomes a real cloud router.

## Official Documentation

- [MikroTik CHR Download](https://mikrotik.com/download/chr)
- [CHR Licensing — MikroTik Manual](https://manual.mikrotik.com/docs/getting-started/routeros-licensing/chr/chr-licensing/)
