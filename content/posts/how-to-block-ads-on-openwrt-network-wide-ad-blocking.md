---
title: "How to Block Ads on OpenWrt | Network-Wide Ad Blocking"
date: 2026-11-05
slug: how-to-block-ads-on-openwrt-network-wide-ad-blocking
categories: ["OpenWrt", "Youtube Videos"]
youtube_id: lheaAh0YZyk
description: "With OpenWrt, you can block advertising and tracking domains across your network using the Adblock package, without installing a separate Pi-hole server or configuring ad blockers on individual devices."
---

Every device on your network shows ads. Phones, tablets, smart TVs, anything with a browser. You could install an ad blocker on each one, or run a separate Pi-hole server. Or you can block the ad domains once, on the router, for every device at the same time.

That is what this lab does. I install the Adblock package on an OpenWrt router, configure it, and test it on a real network.

## What We Are Building

One OpenWrt router that answers DNS for the whole network and refuses to resolve advertising and tracking domains. A blocked domain returns NXDOMAIN, so the device never reaches the ad server.

The plan:

- Install tcpdump and the Adblock package
- Set the startup trigger, the DNS report, and force local DNS
- Pick the blocklists
- Test with the adblock test page and the DNS report
- Add your own domains to the allow and block lists

My router is an Asus running OpenWrt 25.12, the latest stable release. If you run an older OpenWrt version, the steps are exactly the same.

## Before You Start

Adblock works with DNS-based blocking. It is compatible with the different DNS backends on OpenWrt. By default, OpenWrt uses dnsmasq, and my setup is the default, so I change nothing there. If you changed your DNS backend, you need to select it in the Adblock settings too.

There are four different ad-blocking packages for OpenWrt, and all of them work. This video uses adblock. At the end I explain why I picked it over AdGuard Home.

## Step 1: Update the Package Lists

In LuCI I open System, then Software. The first step is to update the repository list on the router. I click Update lists and wait a few seconds, then click Dismiss.

Expected result: the package list is updated and ready to search.

## Step 2: Install tcpdump

The DNS report needs tcpdump. In the Available tab I search for tcpdump. There are two options: tcpdump and tcpdump-mini. If your router has a weaker CPU, install tcpdump-mini. I install the full tcpdump.

I wait a few seconds, it finishes, and I click Dismiss.

Expected result: tcpdump shows as installed.

## Step 3: Install Adblock

Next I search for adblock. Five packages appear. The core package is the first one, adblock. But since I use the LuCI web interface, I install luci-app-adblock. Installing it pulls in the core package as a dependency.

I click Install, then Install again, and wait a few seconds. Both packages install. I click Dismiss, and after a few seconds they show in the Installed list.

Then I refresh the page. A new menu appears under Services: Adblock.

Expected result: Services has an Adblock entry, and the Adblock dashboard opens.

## Step 4: Set the Basic Options

The dashboard has tiles for service status, blocked domains, last run, and other information. Under the run information I can see the paths of the files Adblock uses on the router.

In General Settings, the service is enabled by default. I set the startup trigger interface to WAN. I also enable the DNS report, which is why I installed tcpdump earlier. The report appears after the service runs.

There is an option to allocate CPU cores to the service. I leave it alone.

Then the firewall settings. This part matters. After this setup, the DNS server of the clients in your network should be the IP address of the router. But what if a client sets another DNS server? Then it never queries the router, and it bypasses the whole policy.

Force local DNS fixes that. It redirects the queries to the router, and the router answers them, even if the client set a different DNS server. I check that option, select my local interface, which is the LAN bridge, and set the force ports to the default DNS port, 53.

Next I set the reporting interface to the LAN bridge as well. I skip the advanced email settings, which are only for reporting.

Expected result: the basic settings are in place, ready to save.

## Step 5: Pick the Blocklists

The last setting is the list of sources. By default, OpenWrt selects AdGuard, AdGuard tracking, and certpl. You can pick one of them or several, based on what you need.

You can also use the Steven Black list. I introduced it in an earlier video about blocking ads on MikroTik RouterOS, and it works here too. And the IPFire list offers different categories, so you can block ads, dating, or other specific categories only.

I keep the default selection for this lab.

Then I click Save and restart and wait. How long it takes depends on your CPU. On my router it takes about 30 seconds.

Expected result: the service is enabled, and the dashboard shows about 190,000 blocked domains.

## Step 6: Test It

Now I test. In the DNS report tab I click the adblock test button. It opens the adblock test website, and after a few seconds the summary appears: it blocked 110 domains out of 132.

Then I go back to the report dashboard and refresh. The first time, report generation fails. The dashboard says it failed to generate the adblock report. I restart the service once more with Save and restart, wait a few seconds, and rerun the test.

This time the report is generated. Total queries: about 180. Block rate: about 90%.

The report shows the top allowed domains and the top blocked domains, the clients by number of queries, and a detailed line for every single query: time, date, client IP address, interface, record type, domain, and result.

Some allowed domains in my report: Facebook, Instagram, google.com, and itunes.apple.com. Some blocked ones surprised me. studio.youtube.com is in the block list, and I do not know why. Blocking is a list decision, not a judgment about the site, so a domain you actually use can land on a list. That is what the allow list is for.

Expected result: the test page shows most ad domains blocked, and the DNS report shows real queries with a block rate near 90%.

## Step 7: Add Your Own Domains

The lists are a starting point, not the final word. You can edit them from the report or from the allow and block list tabs. Each domain goes on its own line.

From the report, I click a domain and add it to the block list. I do this with my own domain as a demo: from now on, nobody on my network can open it.

I also allow a blocked domain. I add googletagmanager.com to the allow list and click Save.

After changing the allow or block list, you need to reload the service. I go back to the Overview tab and click Save and reload, then wait a few seconds.

Then I test with nslookup. The allowed domain is not blocked by my DNS server. My own domain now returns NXDOMAIN. That works.

One honest note on the test: the allowed domain returned no answer at all in nslookup. The DNS server did not block it, but there was a different problem with that domain, so that part of the test was inconclusive. Test with different domains and check the report, not just one lookup.

Expected result: the blocked domain returns NXDOMAIN, and the allowed domain is no longer blocked.

## Why Adblock and Not AdGuard Home

I tested AdGuard Home on this router too. It works well, and its configuration is much simpler. The problem was CPU load. It put a heavy load on my router, so I switched to Adblock.

Adblock does the same job with less load on the router. If your router has the CPU headroom, AdGuard Home is a fair choice. On mine, Adblock is the one that stays.

## Final Thoughts

For a home network, this is the right shape for ad blocking. One place, one set of lists, every device covered. No per-device setup, no extra server.

The setup takes a few minutes, the test page gives you a number you can trust, and the report shows you exactly what is being blocked and what is not. When a list blocks something you need, the allow list is one click away.

Just keep the scope in mind. This blocks domains at DNS level. It does not remove ads served from the same domain as the content, and it does not replace a browser ad blocker for everything. But for network-wide blocking with a light footprint on the router, it does the job.

## Official Documentation

- [OpenWrt Adblock package README](https://github.com/openwrt/packages/tree/master/net/adblock)
