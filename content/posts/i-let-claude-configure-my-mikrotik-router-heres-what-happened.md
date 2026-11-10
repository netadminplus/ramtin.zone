---
title: "I Let Claude Configure My MikroTik Router. Here’s What Happened"
date: 2026-09-24
slug: i-let-claude-configure-my-mikrotik-router-heres-what-happened
categories: ["MikroTik", "AI×Networking", "Youtube Videos"]
youtube_id: 19ryjVKr1JU
description: "In this video, I test whether Claude AI can actually configure a MikroTik router. Instead of manually configuring RouterOS myself, I give Claude SSH access to a MikroTik router and let it build a complete network configuration based on a real-world scenario."
---

Can AI take control and configure a router for us? As a network engineer, my first instinct is no. I would not trust it. But instinct is not a test. So I ran one.

In this video, I give Claude Code SSH access to a MikroTik router with a default configuration, and I let it build a complete network: three Wi-Fi networks, a VPN, a hotspot, firewall rules, and network isolation. Then I check everything it did, and I test the networks for real.

## What We're Doing

Claude has to build all of this, on a real router, over SSH:

- A main Wi-Fi network with normal internet access
- A VPN network, where traffic goes out through an L2TP VPN connection
- A guest network with MikroTik Hotspot authentication, isolated from the other two
- DHCP, DNS, NAT, routing, policy routing, firewall rules, and bridges to hold it together

This is not a prompt that asks for commands to paste. Claude has to inspect the router, configure it, fix problems as they come up, and validate the result. The full prompt is in my Telegram channel, linked in the video description, so you can read it and adapt it.

## Before You Start

The test router sits in my home network with a default configuration. It connects to my home router through ether1. My laptop connects to its Wi-Fi, and that Wi-Fi is also my internet connection. That detail matters, and it causes trouble later.

I run Claude Code inside VS Code, logged in to my Claude account. I use the Opus model, with effort set to medium, and I run it in auto mode, which lets Claude act without asking first. That is fine for a test router. On a production device, I would not do that. Plan mode is the safer choice: Claude shows the full plan first, and only continues after I approve it. There is also an ask-before-edits mode, where Claude shows each command and waits for confirmation.

The prompt itself has a few rules worth stealing. It tells Claude to work from the exact RouterOS version on the router and the official MikroTik documentation. It describes the starting topology and the target network. It sets a workflow that protects the management connection, because changing the Wi-Fi config can cut off my own laptop. It asks for backups saved into the VS Code project folder, not only on the router. And it asks for validation, troubleshooting, and a final report in Markdown, so I can compare the report against the real config.

## Security First, Before Claude Touches Anything

The default config leaves every service port open. For my setup, that is acceptable, because the router sits behind my home router and behind CGNAT, with no public IP address on it. On a router with a public IP, it is not acceptable.

If you try this, be careful with the management path. Change the service ports from their defaults, and restrict which IP addresses can reach each service. Do not use Telnet. SSH is secure, fast, and the right choice here. API or SSL are options too, but plain HTTP is not one I suggest.

I gave Claude a full-access user, and that user was the only one on the router. A cleaner way is to create a separate full-access user just for the test, and disable it when the work is done. Either way, change the admin username and password after the configuration is done, and change the Wi-Fi passwords too. I say this twice in the video, because it is the kind of step people skip.

## Step 1: Paste the Prompt and Let It Work

I open a test folder in VS Code, open the Claude Code extension, paste the prompt, and submit it. The prompt covers the core rules, the RouterOS version, the starting topology, the target networks, the L2TP VPN, the guest hotspot, the custom login page, the firewall, management safety, backups, the workflow, and the validation and report at the end.

Claude starts by inspecting the router over SSH: the current config, the RouterOS version, and the hardware. Then it begins building the three networks.

Expected result: Claude reads the router state first, then starts configuring, instead of guessing.

## Step 2: The Hotspot Cuts Off My Internet, Twice

This is the part I expected. My laptop reaches the internet through the test router's Wi-Fi. When Claude reconfigures that Wi-Fi, my connection drops.

The first break shows up as an API error in Claude Code. My laptop had connected itself to the new hotspot network, and the hotspot login page appeared. Without logging in, there is no internet. I log in with a hotspot user, and Claude has internet access again.

It happens a second time. The laptop drops off the hotspot network while Claude tests the new Wi-Fi, then joins it again, and I log in once more. After that, I connect the laptop back to the main Wi-Fi network, and Claude continues.

If I had a cable between my laptop and the router, this would not have happened. The Wi-Fi path was the weak point, and the prompt's workflow rules were written for exactly this case.

Expected result: two interruptions, both fixed by logging in to the hotspot and reconnecting, and Claude picks up where it left off.

## Step 3: Read Claude's Report

When Claude finishes, it writes a short summary and a full report in Markdown, saved in the VS Code folder. The report lists the router model and RouterOS version, the target design, a network diagram, IP addressing, interface mapping, bridges, DHCP, DNS, routing, and policy routing.

One detail in the report is worth noting. The router has only one Wi-Fi 6 radio, so Claude used virtual APs to create the three Wi-Fi networks. That is the right call on this hardware.

Claude also saved backups: a config export and a backup file, both in the project folder, not only on the router.

Expected result: a full written report plus export and backup files I can check against the router.

## Step 4: Verify the Config in WinBox

A report is a claim. I check it against the router.

In Wi-Fi, there are three interfaces: one for the main network, one for the VPN network, and one for the guest network. The L2TP VPN client shows as connected. In IP, then Addresses, the three networks have the addresses I asked for. In DHCP Server, the networks and servers are there. In IP, then Pool, the pools Claude created are there.

In the firewall filter rules, next to the default hotspot rules, there are new rules with comments, as I asked. In NAT, there are new rules next to the default hotspot rules. In Mangle, there is a rule with a new routing mark, and in Routing, then Tables, the new table is there. In that table, the default route points at the L2TP VPN interface.

I did a quick check, not a full audit. I found no mistake in what I looked at. But that is the point I want to be clear about: a quick look is not a full review. If you let an AI configure a router, take the time to read all of it before you trust it.

Expected result: every piece I asked for is present, with the routing mark and the VPN table wired up correctly.

## Step 5: Test the VPN Wi-Fi

The last test is the one that matters most. I open iplocation.com on the main Wi-Fi, and my public IP is in Iran. Then I switch to the VPN Wi-Fi network and open the same page. My public IP is now in Germany, which is where my VPN server sits.

The hotspot needs no separate test. I already watched it work twice during the setup, when the login page appeared and the custom login page loaded.

Expected result: main Wi-Fi shows an Iran IP, VPN Wi-Fi shows a Germany IP.

## Final Thoughts

Claude did the job. Three networks, VPN routing, hotspot, firewall rules, backups, and a readable report. And it recovered from the connection breaks on its own.

I will still say this plainly: it was a simple setup. As a network engineer, I can build it by hand in under ten minutes. That is not the point. The point is what happens when the device in front of you is one you do not know well. You can take the AI into the lab, let it build the config, study what it did, and only then move the result to production.

Two rules make that safe. First, know what you want before you start. You cannot rely on AI to make the network design decisions for you. Second, lab first, production later. The basics are yours to know. The commands and the details are what you can lean on the AI for.

## Official Documentation

- [Claude Code Overview](https://code.claude.com/docs/en/overview)
- [RouterOS Documentation](https://help.mikrotik.com/docs/)
