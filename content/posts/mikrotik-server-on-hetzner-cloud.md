---
title: "Install MikroTik Server on Hetzner Cloud"
date: 2026-01-19
slug: mikrotik-server-on-hetzner-cloud
categories: ["MikroTik", "Youtube Videos"]
youtube_id: 0hX-v1LNYtU
image: /assets/images/Run-MikroTik-Server-on-Hetzner-netadminhub.com_.webp
description: "Running a MikroTik router in the cloud gives you incredible flexibility for VPNs, routing, and lab environments."
migrated_from: netadminhub.com
---

Running a MikroTik router in the cloud gives you incredible flexibility for VPNs, routing, and lab environments. But if you’ve looked at the Hetzner OS list, you’ll notice MikroTik is missing.

Don’t worry—getting MikroTik Cloud Hosted Router (CHR) running on Hetzner is actually very easy. Whether you like getting your hands dirty in the terminal or you prefer a “set it and forget it” automation, I’ve got you covered.

Watch the full video walkthrough over at the [Net Admin HUB YouTube channel](https://youtu.be/0hX-v1LNYtU)!

## Why Hetzner for MikroTik?

- **Insane Traffic:** Most plans include 20TB of traffic—perfect for a high-bandwidth VPN or bridge.
- **Low Latency:** With data centers in Germany, Finland, and the US, you can pick a location close to your users.
- **Price:** You can run a stable MikroTik instance for just a few euros a month.

## Method 1: The Manual Linux Way

If you already have a Linux server running or want to see exactly what’s happening, use this method.

### Step 1: Spin up a Small Ubuntu Server

Create a new server on Hetzner choosing **Ubuntu 22.04**. The smallest “Shared vCPU” plan is more than enough for RouterOS.

### Step 2: Download and Flash the Image

SSH into your new server and run these commands to download the MikroTik CHR raw image and write it directly to your disk:

```
# Download the image
wget https://download.mikrotik.com/routeros/7.x.x/chr-7.x.x.img.zip

# Extract it
gunzip -S .zip chr-7.x.x.img.zip

# Write to disk (Check your disk name, usually sda or vda)
dd if=chr-7.x.x.img of=/dev/sda bs=4M oflag=sync
```

### Step 3: Reboot

Type `reboot`. In a few seconds, your Ubuntu server will be replaced by a fresh MikroTik RouterOS.

## Method 2: The Pro Way (Automated Cloud-Config)

This is my favorite. You don’t even need to SSH into Linux. You just paste a script, and Hetzner does the work for you.

1. Click **Add Server** in Hetzner.
1. Scroll down to **Cloud-config** (User Data).
1. Paste the YAML script (available in our Telegram community) that downloads and installs the image automatically.
1. Hit **Create**, and by the time the server status turns green, it’s already a MikroTik router.

## Critical: Don’t Get Hacked!

As soon as your MikroTik is live, it has a public IP and **no password**. Bots will find you in seconds.

1. **Set a Password immediately** via WinBox or Terminal.
1. **Disable Unused Services:** Go to `IP > Services` and disable `ssh`, `telnet`, and `ftp` if you don’t need them.
1. **Change Ports:** If you keep WinBox open, move it from the default `8291` to something custom.

## The “Unlimited” Trial Secret

When you install CHR, you start with a **Free** license, which limits you to 1Mbps. That’s useless for most things.

**Tip:** Head over to `System > License` and sign in with your MikroTik account to start your 60-day trial. You can choose any level—P1, P10, or even P-Unlimited—to unlock full speed.

The cool part? After 60 days, MikroTik doesn’t actually throttle your bandwidth—you’ll keep your full speed. The only catch is that you won’t be able to upgrade your RouterOS version anymore. **Feature****Recommendation****OS Choice****CPU Arch****License Level****Security**

|  |  |
| --- | --- |
|  | Ubuntu 22.04 (for manual) or Cloud-Config |
|  | x86 (Standard for CHR) |
|  | P1 or P10 (Trial available) |
|  | Disable Telnet/SSH immediately |
