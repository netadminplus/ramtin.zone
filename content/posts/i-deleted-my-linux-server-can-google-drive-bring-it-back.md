---
title: "I Deleted My Linux Server. Can Google Drive Bring It Back?"
date: 2026-10-10
slug: i-deleted-my-linux-server-can-google-drive-bring-it-back
categories: ["Tips & Tricks", "Youtube Videos"]
youtube_id: RkhyYrpAC8w
description: "Can you use Google Drive as remote backup storage for your Linux server? In this video, I test exactly that using Rclone, an open-source tool for transferring files between local systems and cloud storage services."
---

I upgraded my Google account to AI Pro, and with it came 5 TB of Google Drive storage. That space was just sitting there. So I asked a simple question: can it hold the backups of my Linux server? And if the server dies, can those backups bring it back?

That is the test in this video. I connect the server to Google Drive with Rclone, upload the backups, delete the whole server, build a fresh one, and restore everything from Drive.

## What We're Doing

- Connect a Linux server to Google Drive with Rclone
- Upload the server backups to a folder on Drive
- Verify the upload, file by file
- Delete the VPS and build a fresh Ubuntu server
- Download the backups, restore the stack, and point DNS at the new server
- Check that the services work again

One thing this video does not cover: the backup system itself. It already exists on my server, and it works. If you want a full video about building a trusted backup system on Linux, that is a separate topic.

## Before You Start

My server runs a small Docker Compose stack: Caddy as the reverse proxy, Nextcloud, Gitea, and a PostgreSQL database, all from a single compose file. The backup system stores finished backups in a `completed` directory on the server. I already have two completed backups there. Each one holds an archive file, a JSON file for validation, and a checksum file.

The plan only works because the local backups are good. A remote copy of a broken backup is still a broken backup. If you run a database, think about backup timing for your own project, so a restore gives you data you can trust.

I also did not automate the upload in this video. No cron job, no systemd timer. The upload here is manual, one command at a time, so the test stays easy to follow.

## Step 1: Set Up the Google Cloud Project

Rclone cannot just log in to Drive on its own. It needs an OAuth client, and that means a short visit to the Google Cloud Console.

I open console.cloud.google.com, create a new project, and name it `backup`. Inside the project, I open APIs and Services, then Library, search for the Google Drive API, and enable it.

Next is the OAuth consent screen. I click Get started, name the app `Rclone`, set my own email as the support email and the contact email, pick External as the audience, agree to the terms, and create it.

Then I create the OAuth client: application type Desktop app, name `Rclone` again. Google gives me a client ID and a client secret. I keep those somewhere safe, because Rclone will ask for them in the next step. I also download the JSON file Google offers.

One last step on this page: the app is in testing mode, so I add my own email as a test user. Without that, the refresh token resets every seven days, and I would have to connect Rclone again each week. Publishing the app properly is the long-term fix, but a test user is enough for this demo.

Expected result: the Drive API is enabled, the OAuth client exists, and I have the client ID and secret ready.

## Step 2: Install Rclone and Connect It to Drive

Back on the server, I update the package lists and install Rclone:

```
apt update
apt install rclone -y
```

Then I check the version:

```
rclone version
```

It prints the version, so the install worked. Now the connection:

```
rclone config
```

The wizard asks for a new remote. I press `n`, name it `gdrive`, and pick Google Drive from the service list. On my install, Drive is number 13 in that list. Then I paste the client ID and the client secret from the last step.

For the scope, I pick number 1: full access to all files, except the Application Data folder. I leave the root folder ID blank, leave the service account file blank, answer `n` to advanced config, and `n` to auto config. Since the server has no browser, Rclone prints a long link instead. I open that link on my own computer, pick my Google account, agree, and copy the authorization code back into the terminal. Team drive? No. Apply the config? Yes. Then I quit the wizard.

Expected result: `rclone config` shows one remote, named `gdrive`.

## Step 3: Upload the Backups

First, a quick look at what is on Drive already:

```
rclone ls gdrive:
rclone lsd gdrive:
```

The first command lists files, the second lists directories only. Then I make a folder for the backups:

```
rclone mkdir gdrive:backup
```

I check the Drive web page before and after. Before, there is no backup folder. After, there is one. The connection works both ways.

Now the upload. I copy the `completed` backups directory to that folder:

```
rclone copy <local-completed-directory> gdrive:backup --progress
```

The `--progress` flag shows the upload speed and the percentage for each file. After a few seconds, the backup folder on Drive holds the completed backup directories, with the archive files, the JSON files, and the checksum files inside them.

Expected result: the files appear in Drive, in the `backup` folder, with matching sizes.

## Step 4: Verify the Upload

An upload you never checked is a guess, not a backup. So I run a check:

```
rclone check <local-completed-directory> gdrive:backup --one-way
```

The `--one-way` flag treats the local directory as the source of truth and compares the destination against it. After a few seconds, Rclone reports no differences. Six files match completely. The remote copy is good.

Expected result: zero differences, six files matched.

## Step 5: Delete the Server and Build a Fresh One

Now the real test. I log in to my Hetzner console, delete the old server, and create a new one. The new server gets a new IP address. I log in over SSH, and it is a fresh Ubuntu 22 install.

First, Docker and Docker Compose. I follow the official Docker install docs for Ubuntu and paste the install commands from there. Then I install Rclone on the new server, exactly as before:

```
apt update
apt install rclone -y
rclone config
```

The config wizard runs the same way: a new remote named `gdrive`, Google Drive, the same client ID and secret, scope 1, no auto config, and the browser authorization step again. The client ID and secret live outside the server, in my notes, because the old server is gone.

I check the remote:

```
rclone lsd gdrive:
```

Expected result: the `backup` folder is listed. The new server talks to the same Drive.

## Step 6: Download, Restore, and Point DNS at the New Server

I download the backups:

```
rclone copy gdrive:backup <local-completed-directory> --progress
```

The two backup directories land on the new server. I open one, extract the archive, and move the project to the root directory:

```
tar xzvf <archive-file>
cp -r <project-directory> /root
```

Then I start the stack:

```
docker compose up -d
```

Docker pulls the images again, and the containers come up. Meanwhile, I change DNS in Cloudflare to the new server IP. DNS checkers show the new address within seconds for one subdomain, and the other follows shortly after.

Expected result: the stack runs on the new server, and the domains point at its new IP.

## What Went Wrong

Two things did not go smoothly, and both are worth naming.

First, after the restore, I lost SSH access to the new server from my terminal. The stack itself was up and running, and I could reach the server through the Hetzner web console, but SSH from my machine would not connect. I reset the root password from the Hetzner console, logged in through the console, and after that, SSH worked again. I still do not know what caused the break. I will not guess at a cause here.

Second, the Nextcloud container was still starting when I first checked the services. It needed more time before it was ready. The Gitea login page and the other subdomain loaded fine in the meantime. A container that says it is up is not always a service that is ready to answer.

One more note: I removed this test server after the recording. The passwords shown in the video were for the demo only.

## Final Thoughts

It worked. Google Drive held the backups, and a fresh server came back from them with a few commands. The whole restore took minutes, not hours.

But I would not run this in production exactly as shown. Three things are missing. First, encrypt the backup archives before they leave your server. Drive is someone else's computer. Second, automate the upload, with a cron job or a systemd timer, so a backup happens even when you forget. Third, test the restore on a regular schedule, the way this video did, because a backup you never restored is only a hope.

The idea is sound. The 5 TB I already pay for can be one more copy of my backups, next to the local ones. It is a backup of the backups, and that is a good use of space I already have.

## Quick Reference

Commands from this lab:

```
apt update
apt install rclone -y
rclone version
rclone config
rclone ls gdrive:
rclone lsd gdrive:
rclone mkdir gdrive:backup
rclone copy <local-completed-directory> gdrive:backup --progress
rclone check <local-completed-directory> gdrive:backup --one-way
rclone copy gdrive:backup <local-completed-directory> --progress
tar xzvf <archive-file>
cp -r <project-directory> /root
docker compose up -d
```

## Official Documentation

- [Rclone](https://rclone.org/)
- [Rclone Google Drive Guide](https://rclone.org/drive/)
