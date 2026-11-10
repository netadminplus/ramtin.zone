---
title: "How to Configure MikroTik for the First Time: A Clean Step-by-Step Guide"
date: 2026-02-01
slug: mikrotik-first-time-configuration
categories: ["MikroTik", "Youtube Videos"]
youtube_id: FDBhw-TO6vI
image: /assets/images/mikrotik-first-time-configuration-netadminhub.com_.webp
description: "In this guide, I’ll show you how to take a blank MikroTik and turn it into a fully functional, secure gateway."
migrated_from: netadminhub.com
---

Most people unbox a MikroTik, see the default configuration, and think they’re good to go. But let’s be honest: the default config is often cluttered and not always secure.

If you want a network that’s actually built for your needs—and not just “working”—you need to start from scratch. In this guide, I’ll show you how to take a blank MikroTik and turn it into a fully functional, secure gateway.

Watch the full step-by-step walkthrough on the **Net Admin HUB** YouTube channel:

---

## Step 1: Wipe the Slate Clean (Reset)

Before we build, we destroy. Factory settings can cause IP conflicts and unnecessary firewall rules.

1. Navigate to **System > Reset Configuration**.
1. Check **No Default Configuration** and **Do Not Backup**.
1. Click **Reset**.

When the router reboots, it will have no IP. Use **WinBox** and click on the **Neighbors** tab to log in via the MAC Address. Use the login `admin` with a blank password.

**Important Security Tip:** The second you log in, go to **System > Users** and set a strong password. A MikroTik with a public IP and no password is a ticking time bomb.

---

## Step 2: Configure Your WAN (Internet In)

Your router needs to talk to the world. Depending on your ISP, use one of these three methods on your **ether1** port:

### 1. DHCP Client (Automatic)

If you’re behind another modem or router: Go to **IP > DHCP Client**, click `+`, select `ether1`, and ensure **Add Default Route** is set to `yes`.

### 2. PPPoE (Fiber/ADSL Bridge)

If your ISP gave you a username and password: Go to **PPP > Interface**, add a **PPPoE Client**. Under the **Dial Out** tab, enter your credentials and check **Add Default Route**.

### 3. Static IP

If you have a dedicated IP:

- **IP > Addresses:** Add your IP (e.g., `1.2.3.4/24`) to `ether1`.
- **IP > Routes:** Add a route with `0.0.0.0/0` and point the gateway to your ISP’s IP.
- **IP > DNS:** Add `8.8.8.8` or your preferred servers.

---

## Step 3: Create Your Local Network (LAN)

Now, let’s make sure your devices can talk to each other.

1. **The Bridge:** Go to **Bridge**, create a new one named `bridge-LAN`. In the **Ports** tab, add all other ports (`ether2` to `ether5`) to this bridge.
1. **Assign IP:** Go to **IP > Addresses** and give the bridge an IP, like `192.168.88.1/24`.
1. **DHCP Server:** Go to **IP > DHCP Server** and click **DHCP Setup**. Select `bridge-LAN` and click “Next” until finished. Your devices will now get IPs automatically.

---

## Step 4: Enable NAT (The “Internet” Rule)

Your devices have local IPs, but they can’t browse the web yet. We need **NAT (Network Address Translation)** to mask your local traffic behind your public IP.

Go to **IP > Firewall > NAT** and add a rule:

**Action:** `masquerade`

**Chain:** `srcnat`

**Out. Interface:** `ether1` (or your PPPoE interface).

## Summary Table for Quick Setup **Step****Action****Path in WinBox****1****2****3****4****5**

|  |  |  |
| --- | --- | --- |
|  | Reset (No Default) | System > Reset |
|  | Set Admin Password | System > Users |
|  | Setup WAN | IP > DHCP Client / PPP |
|  | Bridge LAN Ports | Bridge > Ports |
|  | Activate NAT | IP > Firewall > NAT |

## Final Thoughts

Setting up a MikroTik for the first time might seem intimidating, but once you understand the flow—Reset, WAN, LAN, NAT—it becomes second nature.

**Want to dive deeper into MikroTik security?** Check out my other posts on Ramtin Tech Zone or join the conversation on our Telegram channel!
