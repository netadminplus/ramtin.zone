---
title: "How AI Agents Actually Work (Explained Simply)"
date: 2026-10-16
slug: how-ai-agents-actually-work-explained-simply
categories: ["AI×Networking", "Youtube Videos"]
youtube_id: saac7rGcObQ
description: "How do AI agents actually work? What makes them different from AI chatbots and traditional automation workflows? In this video, I explain how AI agents work behind the scenes, from large language models (LLMs) and tool calling to the agent loop, RAG, MCP, and security."
---

AI agents are everywhere now. But how do they actually work, and what makes one different from a regular chatbot?

The short answer: an agent is not a smarter chatbot. It is a system built around a language model, and the model is only one part of it. This article walks through that system, one piece at a time, using a server troubleshooting example.

## Start with the Model

Everything starts with a large language model, an LLM. GPT, Claude, Gemini, Qwen: different companies, same basic idea.

A model takes an input, like a question about an HTTP error, and generates output piece by piece, predicting what comes next. Each piece is a token. On a slide a token looks like a word, but in reality tokens are often parts of words.

That sounds like autocomplete. It is more than that. From a huge amount of training data, the model learns patterns of language, code, and reasoning. So it can explain an error it has never seen. It is not looking up a stored answer.

But a model has two hard limits.

The first is knowledge. The model knows what it learned in training, plus whatever you give it in the request. Your server information, your configuration, your logs: none of that is visible to the model unless someone provides it.

The second is action. A model generates output: text, code, or structured data. It might generate a correct command, like `systemctl restart nginx`. But generating a command is not executing it. The model runs nothing on your server.

## From a Model to a Chatbot

ChatGPT is not a model. It is an application built around a model. That distinction matters, because the application adds the parts the model lacks.

When you send a message, the chat application builds a request: instructions from the vendor, the conversation so far, and your new message. It sends that to the model, gets the response, and shows it back to you.

The conversation history matters here. The model does not remember your earlier messages. Each request is independent. The application keeps the history and sends the relevant part, or a summary, with every new message.

Take a web server returning errors. You ask the chatbot for help. It suggests `systemctl status nginx` to check the web server. You run it and paste the output back: the status is active and running. The chatbot reads that and suggests the next command, checking the error log. You run it again and paste again.

The model does the thinking. You are the execution layer.

## Tool Calling: How Software Runs the Command

So why can't these systems run the commands themselves? They can. But not by letting the model type into your terminal. It works in five steps.

First, the application describes a set of tools to the model. Each tool has a name and its inputs. In our example: check service, read log, read file.

Second, when the model needs information, it produces a structured request. For example: check service, nginx.

Third, and this is the most important point in the whole video: that request is not an action. Nothing has happened on the web server yet.

Fourth, the application checks the permission. Is this tool allowed? If it passes, the application executes real code against the web server.

Fifth, the result goes back to the model in the next request.

That is tool calling. The model requests, and software executes. Even when a vendor runs a tool on its side, like a web search, software does the execution, not the model.

## The Agent Loop

Troubleshooting is rarely one step. You check something, look at the result, and decide what to check next. That is a loop, and it is the core of most AI agents.

The model sends a tool request. The application executes it, gets the output, and sends the result back into the context. Then the model is called again. Note that the web server never talks to the model directly. The application sits in the middle.

Here is one complete run. The goal: find out why the web server returns an error, which usually means nginx could not get a valid response from the backend.

The model checks the obvious thing first: is nginx running? Yes. So the problem is behind nginx. The error log says: connection refused to port 8080. Something should be listening there, and it is not.

Which service is that? The nginx config points proxy_pass at an upstream called web app, which is the backend service on this server. The model checks it. It has failed. Its log says: port 8080 is already in use.

That is enough evidence. The model stops calling tools and writes the final answer: another process holds the required port, so identify the process and resolve the conflict before restarting web app.

Nobody scripted that sequence. If nginx had been down, every next step would have been different. The model observes a result, reasons, and chooses the next action. That cycle is the agent loop.

The loop needs a clear end. Normally it ends with a final answer. But a model can get stuck, so the system should limit steps, time, and cost. A production change, like a restart, waits for human approval.

## Who Decides the Next Step?

Not every AI system that uses tools is an agent. The better question is: who decides the next step?

With a chatbot, you decide. With a workflow, the steps are designed in advance: an alert arrives, an LLM classifies it, and the workflow routes it. The LLM decides, but only inside one fixed step. Scripts and scheduled jobs work the same way, without an LLM.

With an agent, the model chooses the next step from the results it gets back, within the defined limits.

These boundaries are not sharp. Many real systems are hybrids. And moving toward more autonomy is not free. More autonomy gives you more flexibility, but less predictability. More cost, and more testing.

## The Parts of an Agent System

In the middle sits the LLM. It reasons and makes requests, but it is only one component.

Around it is the harness. You may also hear runtime or orchestrator, and there is no single agreed definition. The harness is the software that runs the loop. It builds the context, calls the model, executes tools, enforces limits, and logs activities.

The context is everything the model sees in one call: instructions, the goal, tool descriptions, and the results so far. It is rebuilt for every request, it grows with every step, and it has a size limit.

The tool layer runs only approved requests, and the tools connect to real systems.

At the bottom is optional memory. If an assistant remembers your preferences next week, the application saved that information and brought it back into a later context. Some agents have memory, some do not. The chatbots you use every day, like ChatGPT or Claude, offer this option.

The harness can also bring in knowledge before the model answers. That is RAG, retrieval-augmented generation. Someone asks how to renew a certificate. The model does not know your procedure, so a search system finds the relevant runbook section in your network documentation, adds that text to the context, and the model writes its answer from that information.

Retrieval and generation are separate jobs. Search finds the information, the model writes the answer. If retrieval finds the wrong runbook, the model may produce a confident wrong answer.

RAG does not need a vector database. A simple keyword search can find the relevant documents and pass that information to the model. And using a tool does not automatically mean you are using RAG. Checking whether a service is running is a regular tool call, not RAG.

## Security: Control Lives Outside the Model

Who can stop an agent from doing something wrong? Say you are a network admin, responsible for important infrastructure, and your agent is doing something dangerous.

A common first answer is an explicit instruction: never restart production services. That guides the model, but it enforces nothing. The model can still request it, and the request may be applied.

Real control happens outside the model, in layers. The model requests an action, for example disabling a user. First, the harness checks whether the request is valid and allowed. For sensitive actions, human approval may be required, based on your design.

Next, the tool runs with limited permissions. Even if the request reaches the target system, the system checks permissions too. In this example, the directory rejects the request because the account does not have enough permissions.

Security does not depend on one check or one prompt. Multiple layers work together. That is defense in depth.

Another risk is prompt injection. Agents read emails, tickets, and web pages, and those may contain malicious instructions. The model might follow them. Permissions can block unauthorized actions, but they cannot prevent every mistake. So agents need limited access, and sensitive actions need human approval.

## MCP, in One Paragraph

MCP, the Model Context Protocol, is an open standard for connecting AI applications to tools and data. Someone builds an MCP server, for example for a ticketing system, and it exposes tools like search tickets. Any compatible application can discover and call those tools through its MCP client.

MCP is not a model, and it is not an agent. It is optional, and tools can also be defined directly in code. But an MCP server is software you are trusting, so give it only the access it needs.

## How You Get Access to a Model

These are access arrangements, not types of agents.

With a subscription, you use a vendor application like ChatGPT, the Claude app, or Gemini. The vendor provides everything. API access is usually billed separately.

An API is for software. Your code, your framework, or your platform calls the model, and you usually pay per use. You provide the application, the tools, and the harness. A third-party provider gives you the model through its own API, but your data goes through that provider, so check their terms.

Or you self-host an open-weight model like Qwen with Ollama or vLLM. Your data stays under your own control, but you run your own hardware and your own updates. And it is just a model, not an agent. You still need to combine it into a system.

## Different Products, Different Jobs

A model like GPT or Qwen is the core engine: no tools, no loop. General assistants like ChatGPT or the Claude app are ready to use, and some features perform tasks with tools. Coding agents like Codex and Claude Code read files, write code, and run commands, with the agent system already built. Automation platforms like n8n let you build workflows by connecting steps, adding AI when needed. Custom agents are built for one specific need, and you configure, secure, and maintain them yourself.

Running code locally does not automatically give you an agent. You still need software that connects the model to tools and manages the loop.

## Do You Actually Need an Agent?

First question: does the task follow clear and fixed steps? Rotating logs or renewing certificates are simple, clear tasks. You do not need an AI agent for them. A script, a cron job, or a workflow does the job.

If it is different, check whether an existing tool already does it. To configure servers, use Ansible playbooks. That is simpler, and you do not need an AI agent for that kind of task.

If it is more complicated, ask whether the task needs custom integrations and decisions made by an AI model. If not, stick with your existing workflow.

If you do need that, a custom agent might make sense. But you need to manage its security, monitor its actions, and control its costs. Start with read-only access, limit the steps, log its actions, and require human approval before any change.

## Final Thoughts

More autonomy does not always mean a better solution. A chatbot, a workflow, and an agent are different tools, and the right one depends on who should decide the next step.

If the steps are fixed, write them down and automate them. If the steps depend on what you find along the way, and you can put real limits and approval gates around the system, an agent earns its place. Everything else is a more expensive way to run a script.

## Official Documentation

- [What is the Model Context Protocol?](https://modelcontextprotocol.io/introduction)
