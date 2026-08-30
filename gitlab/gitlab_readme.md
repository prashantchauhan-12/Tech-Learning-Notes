# GitLab for DevOps — Complete Revision Notes

> Compiled from a hands-on Hindi/Hinglish "GitLab Zero to Hero" tutorial transcript, restructured, translated into English, and enriched with additional context from official GitLab documentation for deeper self-study. Use this as a revision sheet — not a verbatim transcript.

---

## Table of Contents

1. [What is GitLab?](#1-what-is-gitlab)
2. [GitLab vs GitHub vs Bitbucket](#2-gitlab-vs-github-vs-bitbucket)
3. [Account Setup & Onboarding](#3-account-setup--onboarding)
4. [Core Concepts: Groups vs Projects](#4-core-concepts-groups-vs-projects)
5. [Creating and Importing Projects](#5-creating-and-importing-projects)
6. [Authentication: SSH, PAT, SSO](#6-authentication-ssh-pat-sso)
7. [GitLab vs GitHub Terminology Cheat Sheet](#7-gitlab-vs-github-terminology-cheat-sheet)
8. [CI/CD Pipeline Fundamentals](#8-cicd-pipeline-fundamentals)
9. [Variables & Secrets Management](#9-variables--secrets-management)
10. [Artifacts](#10-artifacts)
11. [Runners (SaaS / Instance vs Self-hosted / Project)](#11-runners-saas--instance-vs-self-hosted--project)
12. [Hands-on: End-to-End Deployment Pipeline](#12-hands-on-end-to-end-deployment-pipeline)
13. [Real Errors Faced & How They Were Fixed](#13-real-errors-faced--how-they-were-fixed)
14. [DevSecOps — The Bigger Picture](#14-devsecops--the-bigger-picture)
15. [GitLab CI/CD YAML Cheat Sheet](#15-gitlab-cicd-yaml-cheat-sheet)
16. [GitLab Duo — AI in GitLab (2026 Update)](#16-gitlab-duo--ai-in-gitlab-2026-update)
17. [Further Reading / Official Links](#17-further-reading--official-links)

---

## 1. What is GitLab?

GitLab is a **DevOps/DevSecOps platform** that, like GitHub, gives you Git-based version control and project management — but it ships with **CI/CD built in natively**, so you don't need to install or wire up a separate tool like Jenkins.

Key facts:

- It is a **web-based Git repository manager** with issue tracking, merge requests, wikis, container registry, and CI/CD pipelines all bundled together.
- **Open-source core**: GitLab publishes its source code openly (the "Open Core" model), even though enterprise features are paid.
- **Free for personal use**; team/organization usage requires **Premium** or **Ultimate** paid tiers, or you can self-host for free.
- GitLab has existed far longer than GitHub Actions and is considered more mature specifically for CI/CD, DevOps, and DevSecOps workflows.

### The single biggest differentiator: Self-hosting

| | Can you self-host it on your own server? |
|---|---|
| **GitHub** | No — GitHub.com is always cloud-hosted. Self-hosting requires the paid **GitHub Enterprise Server** edition. |
| **GitLab** | **Yes** — you can `docker run` a full GitLab instance on your own infrastructure, even for free (GitLab Community Edition / self-managed). |
| **Bitbucket** | Similar to GitHub — primarily cloud SaaS, with a separate paid **Bitbucket Data Center** for self-hosting. |

> If you are a DevOps/DevSecOps engineer who owns the entire toolchain (repo → build → test → deploy → security scan) and wants full control (including running it on your own servers), **GitLab is generally the better choice**.

---

## 2. GitLab vs GitHub vs Bitbucket

All three are Git hosting platforms, but each has a "specialty":

| Platform | Primary strength | Owned by |
|---|---|---|
| **GitLab** | CI/CD, DevOps, DevSecOps (security baked into the pipeline) | GitLab Inc. |
| **GitHub** | Open-source collaboration; largest global open-source community | Microsoft |
| **Bitbucket** | Seamless integration with Jira and Confluence (project tracking) | Atlassian |

Other differences called out in the tutorial:

- GitHub popularized **Copilot** for AI-assisted coding; GitLab's answer is its own AI suite, now branded **GitLab Duo** (see [Section 16](#16-gitlab-duo--ai-in-gitlab-2026-update)), which is more specifically tuned for DevSecOps workflows rather than just code completion.
- GitLab is fully **open source**, whereas GitHub's core product is closed source (Microsoft-owned).
- Bitbucket's differentiator isn't self-hosting or CI/CD — it's the tight, native integration with the rest of the Atlassian suite (Jira, Confluence, Trello).

---

## 3. Account Setup & Onboarding

Steps to create a GitLab.com account (same idea applies to any provider):

1. Go to `gitlab.com` → **Sign in / Register**.
2. Register using email or via a social/Google sign-in.
3. **Human verification** (CAPTCHA-style puzzle) — GitLab enforces this because its free tier and self-hosted option are so generous that it's an easy target for bot abuse.
4. **Email verification** — a code is emailed to you.
5. **Phone number verification** — required within the first 3 days of account creation. No credit card is ever asked for; only email + phone are used to prove you are a real human, not to charge you.
6. **Personalization survey**: role (e.g., "DevOps Engineer"), your intended use of GitLab (store code / learn Git basics / CI/CD / migrate from GitHub-Bitbucket), team size, etc. Selecting "DevOps Engineer" tailors the onboarding UI to surface CI/CD-relevant features and helper tips.
7. You'll be prompted to create/import your first project — skip this and follow the structured path below (Groups → Projects) instead of the default wizard.

> **Tip from the tutorial:** When importing a repo, avoid the "Import from GitHub" button if you're new to GitLab — it pulls you back toward GitHub mentally. GitLab has quietly removed that shortcut icon for this reason and instead promotes **"Repository by URL."**

---

## 4. Core Concepts: Groups vs Projects

This is the single most important structural concept to internalize before doing anything else in GitLab.

| GitHub | GitLab | Meaning |
|---|---|---|
| **Organization / Username** (namespace) | **Group** | A container that holds team members + all their repositories |
| **Repository** | **Project** | An individual codebase (what you'd call a "repo" on GitHub) |

- A **Group** = "a collection of team members and their projects." Example: your company might have separate groups like `DevOps`, `Frontend`, `Docs` — each with its own set of projects and its own member access list.
- Anyone added to a Group automatically gets access to **all Projects** inside that Group (unless overridden per-project). This is how GitLab does **team/access management**.
- URL structure comparison:

  ```
  GitHub:  github.com / <username-or-org>        / <repository>
                        (this = "Group" concept)    (this = "Project")

  GitLab:  gitlab.com  / <group-name>             / <project-name>
  ```

- Groups and Projects each have their own **Visibility level**: `Private`, `Internal`, or `Public`. A Public group makes every project inside it viewable by anyone with the link, even without an account.
- Naming collision handling: if a group name (e.g., `tws-devops`) is already taken globally, GitLab will silently append characters/numbers to make it unique — always double-check the final slug in your project URL.

---

## 5. Creating and Importing Projects

Two ways to get a project into GitLab:

### A. Create a blank project
`New Project → Create blank project` → choose a Group → set visibility → (optional) initialize with a README.

### B. Import an existing project (e.g., from GitHub)
`New Project → Import project → Repository by URL` (or the dedicated GitHub/Bitbucket importers where available):

1. Paste the **clone URL** of the source repository (GitHub, Bitbucket, FogBugz, or any other Git URL).
2. Choose the destination Group.
3. Set visibility (should generally match the parent Group's visibility).
4. Click **Create project** — GitLab clones the full history, branches, and tags. This can take anywhere from a few minutes (small repo) to much longer for large repos (the instructor noted ~5 minutes for a 90-days-of-DevOps-sized repo).
5. **Mirroring** (optional): Enable "Mirror this repository" if you want ongoing changes pushed to the *original* repo to automatically sync into GitLab too. Without mirroring, an import is a **one-time snapshot** — future upstream commits will NOT appear automatically.

### Auto DevOps
GitLab has a feature called **Auto DevOps** that can automatically generate a working CI/CD pipeline for a new project without you writing any YAML. It's GitLab-exclusive (GitHub has no direct equivalent). For learning purposes, it's usually switched **off** so you build pipelines manually and understand what's happening.

---

## 6. Authentication: SSH, PAT, SSO

GitLab does **not** support plain username/password Git operations (push/pull/clone) — you must use one of:

| Method | When to use |
|---|---|
| **SSH Keys** | Best for personal machines / servers doing recurring git operations (push/pull/clone) |
| **Personal Access Token (PAT)** | Best when using HTTPS instead of SSH (e.g., CI jobs, scripts, Docker registry login) |
| **SSO (Single Sign-On)** | Used in enterprise setups tied to a central identity provider (Okta, Azure AD, Google Workspace, etc.) |

### Setting up SSH (as demonstrated):
```bash
ssh-keygen -t ed25519          # generate key pair, no passphrase needed for demo use
cd ~/.ssh
cat id_ed25519.pub              # copy the PUBLIC key
```
Then in GitLab: **User Settings → SSH Keys → Add new key** → paste the public key → give it a title and (optional) expiration date → **Add key**.

Once added, standard Git commands work exactly like GitHub:
```bash
git clone git@gitlab.com:<group>/<project>.git
git add .
git commit -m "message"
git push origin <branch>
```

> **Security note:** never commit the *private* key anywhere — it stays only on the machine that needs to authenticate.

---

## 7. GitLab vs GitHub Terminology Cheat Sheet

The underlying Git mechanics are identical between platforms — only the *labels* differ:

| Concept | GitHub | GitLab |
|---|---|---|
| Namespace / team container | Organization (or your username) | **Group** |
| Codebase | Repository | **Project** |
| Code review request | **Pull Request (PR)** | **Merge Request (MR)** |
| CI/CD engine | GitHub Actions | **GitLab CI/CD** (built-in) |
| CI/CD config file | `.github/workflows/*.yml` | **`.gitlab-ci.yml`** (single file, in repo root) |
| Build executor | Runner (self-hosted or GitHub-hosted) | **Runner** (same word, same idea) |

As the instructor puts it: *"Pull Request vs Merge Request is chocolate-eclair vs chocolate-cadbury — different name, same chocolate."*

---

## 8. CI/CD Pipeline Fundamentals

### 8.1 The magic filename
To activate CI/CD in a GitLab project, you only need **one file**, committed to the repo root, with this **exact name**:

```
.gitlab-ci.yml
```

The moment this file exists in a branch, GitLab automatically detects it and starts running pipelines on every push — **no external tool (like Jenkins) needs to be installed**. Breaking the filename down:
- Leading `.` → makes it a **hidden** file (same convention as `.gitignore`, `.env`).
- `gitlab-ci` → tells GitLab this file defines its native CI/CD configuration.
- `.yml` → the file must be valid **YAML** — key–value pairs, indentation-based nesting, no curly braces like a Jenkinsfile, and no Python/Java-style syntax. It looks a lot like a `docker-compose.yml` file for exactly this reason.

The instant you create a new file and name it exactly `.gitlab-ci.yml`, GitLab's "New file" screen unlocks an **"Apply a template"** dropdown — proof that GitLab is pattern-matching on this specific filename to activate CI/CD-specific tooling and starter templates (e.g., templates for Node.js, Docker, Android, Terraform, etc.).

### 8.2 Anatomy: Stages and Jobs

A pipeline is built from two core building blocks:

```
Pipeline
 └── Stage 1 (e.g., build)
      └── Job(s)
 └── Stage 2 (e.g., test)
      └── Job(s)
 └── Stage 3 (e.g., push)
      └── Job(s)
 └── Stage 4 (e.g., deploy)
      └── Job(s)
```

Analogy to Jenkins: `Pipeline → Stages → Steps` in Jenkins maps to `Pipeline → Stages → Jobs` in GitLab.

### How it is actually built, step by step (exactly as demonstrated)

**Step 1 — Declare all your stages up front, in order:**
```yaml
stages:
  - build
  - test
  - push
  - deploy
```

**Step 2 — Add the `build` job first (nothing else exists yet):**
```yaml
stages:
  - build
  - test
  - push
  - deploy

build-job:
  stage: build
  script:
    - echo "This build is done using Docker"
    - docker build -ht .
```
Commit this alone (`Edit .gitlab-ci.yml` → commit message: `Added GitLab CI`, committed directly to `main`) and GitLab **immediately** shows a small pipeline icon next to the commit, and unlocks the **Build** menu on the left sidebar (Pipelines, Jobs, Pipeline Editor, Artifacts, Schedules — all become visible only after a `.gitlab-ci.yml` file exists).

**Step 3 — Add the `test` job:**
```yaml
test-job:
  stage: test
  script:
    - echo "This is testing of our Docker build"
```

**Step 4 — Add the `push` job (note the stage name and job's `stage:` value must match exactly):**
```yaml
push-job:
  stage: push
  script:
    - echo "This is pushing to Docker Hub"
```
> You can also write multiple commands as separate lines under `script:` (a YAML list) instead of chaining them — this is cleaner than the equivalent multi-flag single line you'd write in a Jenkinsfile.

**Step 5 — Add the `deploy` job:**
```yaml
deploy-job:
  stage: deploy
  script:
    - echo "Deploying to EC2 instance"
```

**Final, complete file after all 4 steps:**
```yaml
stages:
  - build
  - test
  - push
  - deploy

build-job:
  stage: build
  script:
    - echo "This build is done using Docker"
    - docker build -ht .

test-job:
  stage: test
  script:
    - echo "This is testing of our Docker build"

push-job:
  stage: push
  script:
    - echo "This is pushing to Docker Hub"

deploy-job:
  stage: deploy
  script:
    - echo "Deploying to EC2 instance"
```

Commit message used for the final version: `Edit .gitlab-ci.yml`. As soon as this is committed (directly to `main`/`master` is fine for a demo), go to **Build → Pipelines** and you'll see the pipeline auto-triggered with all 4 stages visible, and clicking into it shows each stage's job status and console output live.

Key rules:
- The **job name** (e.g. `build-job`) can be anything you want — it's just a label.
- The **`stage:` value inside a job MUST exactly match** one of the names listed under the top-level `stages:` list, or the pipeline will error out.
- `script:` accepts a single line or a YAML list of multiple shell commands — keep it clean by breaking multi-step logic into a list.

### 8.3 Where pipelines run and how to view them

Once `.gitlab-ci.yml` is committed:
- Go to **Project → Build → Pipelines** — every push triggers a new pipeline run automatically.
- Click a pipeline to see a visual graph of stages → jobs, their status (running/success/failed), and logs.
- **Pipeline Editor** (Build → Pipeline Editor) gives you a guided YAML editor with lint/validation — it will flag YAML syntax errors (e.g., misspelling `stage` as `stages` inside a job) before you even run anything.
- **Validate Pipeline** button lint-checks your YAML without running it.
- **Web IDE**: a full VS-Code-like in-browser editor for the whole repository, with an integrated source control panel to edit and commit directly from the browser.

### 8.4 Parallel Jobs

Multiple jobs can share the **same stage name** and will run **in parallel** (concurrently), as long as your runner has capacity. This is extremely useful for running the same test suite across multiple environments simultaneously:

```yaml
dev-test-job:
  stage: test
  script:
    - echo "Tested for Dev"
  tags:
    - dev

prod-test-job:
  stage: test
  script:
    - echo "Tested for Prod"
  tags:
    - dev
```
Both jobs are in the `test` stage, so GitLab fires them off at the same time rather than sequentially — dramatically speeding up multi-environment testing.

---

## 9. Variables & Secrets Management

Variables let you avoid hardcoding values (and, critically, avoid exposing secrets) inside your YAML.

### Where to define them
`Project → Settings → CI/CD → Variables → Expand → Add variable`

### Types available
| Property | What it does |
|---|---|
| **Protected** | Variable is only exposed to pipelines running on **protected branches/tags** |
| **Masked** | Value is hidden (`****`) in job logs, even if accidentally echoed |
| **Expanded** | Allows referencing other variables inside its own value |

### Two variable sources in a job:
1. **User-defined variables** — created by you, either directly inside the YAML as a `variables:` object, or at the Project/Group CI/CD Settings level (for secrets).
2. **Predefined (built-in) GitLab variables** — automatically available in every job, no setup needed.

### 9.1 Predefined variables demonstrated in the video

You can Google **"GitLab predefined CI/CD variables"** to get the full list. The ones actually used/shown on screen:

| Variable | What it holds |
|---|---|
| `$CI_PROJECT_NAME` | Name of the current project (e.g., `demo-cicd`) |
| `$CI_JOB_STAGE` | The stage name the currently-running job belongs to |
| `$CI_COMMIT_AUTHOR` | Who authored the commit that triggered this pipeline |
| `$CI_COMMIT_BRANCH` | The branch this pipeline is running on |
| `$CI_COMMIT_MESSAGE` | The commit message that triggered the pipeline |
| `$CI_COMMIT_TAG` | The Git tag, if the pipeline was triggered by a tag |
| `$CI_RUNNER_DESCRIPTION` / runner info | Which runner picked up this job |

Example usage shown on screen, inside the `build-job`:
```yaml
build-job:
  stage: build
  script:
    - echo "$CI_PROJECT_NAME build is done using Docker command"
    - docker build -ht .
```
Output in the job log: `demo-cicd build is done using Docker command` — proving the variable was substituted at runtime.

Another example, inside `test-job`, to show *who* triggered the build:
```yaml
test-job:
  stage: test
  script:
    - echo "This is testing of our Docker build done by $CI_COMMIT_AUTHOR"
```

### 9.2 User-defined variables written directly in YAML (non-secret values)

```yaml
variables:
  DEPLOY_ENV: "production"
  GITLAB_USER_KEY: "This is my secret key"
```
> **Syntax note (important):** this is a YAML *mapping* (`key: value`), not a YAML *list* — so, unlike the `stages:` list above, there is **no leading dash (`-`)** before each variable name. This is the exact same pattern used for the `environment:` block in a `docker-compose.yml` file.

Referencing it later in a job:
```yaml
deploy-job:
  stage: deploy
  script:
    - echo "Testing for production using $GITLAB_USER_KEY"
```

### 9.3 Secret variables (Project-level CI/CD Settings) — full walkthrough

Never hardcode real secrets (passwords, tokens, account IDs) into the YAML file itself — anyone with repo read access could see them in plain text and in the Git history forever. Instead:

**Step 1 — Generate the actual credential.** Example used: a Docker Hub **Personal Access Token**.
`Docker Hub → Account Settings → Personal Access Tokens → Generate new token` → name it (e.g. `gitlab-token`) → permissions: **Read, Write, Delete** → **Generate** → copy the token value immediately (shown only once).

**Step 2 — Store it in GitLab as a masked/protected CI/CD variable.**
`Project → Settings → CI/CD → Variables (expand) → Add variable`

| Field | Value entered |
|---|---|
| Key | `DOCKER_HUB_PASS` |
| Value | *(the Docker Hub personal access token, pasted)* |
| Type | Variable |
| Environment scope | All (default) |
| Protect variable | ✅ (checked) — restricts it to protected branches only |
| Mask variable | ✅ (checked) — so the value never shows in job logs |

Repeat for the username:

| Field | Value entered |
|---|---|
| Key | `DOCKER_HUB_USER` |
| Value | *(your Docker Hub username, e.g.,* `trainwithshubham` *)* |
| Protect | ✅ |
| Mask | ✅ |

> Once saved, **you can never view the value again in the UI** — only overwrite it. This is intentional (same as GitHub Secrets / Jenkins Credentials).

**Step 3 — Use both variables inside the pipeline:**
```yaml
push-job:
  stage: push
  script:
    - docker login -u $DOCKER_HUB_USER -p $DOCKER_HUB_PASS
    - docker tag node:latest $DOCKER_HUB_USER/node-app:latest
    - docker push $DOCKER_HUB_USER/node-app:latest
```
Whenever this job runs, both values are pulled in securely; in the job console output, they always print as `[MASKED]` / `****`, never in clear text — even if you `echo $DOCKER_HUB_PASS` by mistake.

Commit message used for this change: `Added some variable for pipeline`, followed later by `Deploy production using $GITLAB_USER_KEY` when wiring the variable into the deploy job.

### 9.4 Project-level scoping — a real error hit in the video

If a *different* project's pipeline can't find a variable (`$DOCKER_HUB_USER` prints empty, or the whole login step fails), the cause is almost always: **CI/CD variables are scoped strictly to the project they were created in** (unless defined at the parent **Group** level instead, where every project inside the group inherits them). The fix demonstrated:
`Settings → CI/CD → Variables` — go into the **exact project that is running the failing pipeline** and re-add the same `DOCKER_HUB_USER` / `DOCKER_HUB_PASS` variables there too.

There is **no "import variables from another project"** button — GitLab does not support that; you must re-declare them per project (or centralize at the Group level from the start).

---

## 10. Artifacts

**Artifacts** = files generated by a job that you want to **preserve, download, or pass to a later stage** after the job finishes (like saving files to a shared drive, e.g. Google Drive or JFrog Artifactory).

Common use cases: test result logs, build reports, compiled binaries, coverage reports.

### 10.1 Enable artifact retention globally (optional setting)
`Settings → CI/CD → Artifacts (expand) → check "Keep artifacts from most recent successful jobs"` — this is a project-level toggle so artifacts of the latest successful jobs are always retained.

### 10.2 First attempt (as demonstrated) — and the error it produced

```yaml
test-job:
  stage: test
  script:
    - echo "These are my test results" > dlog
  artifacts:
    paths:
      - logs/dlog
    expire_in: 1 week
```
Running this **failed** with:
```
dlog: No such file or directory
```
**Why:** the `logs/` folder referenced in `artifacts.paths` did not exist anywhere on disk — the `script` step wrote a file called `dlog` straight into the working directory, but the artifact path pointed inside a `logs/` folder that was never created. GitLab does **not** auto-create custom-named folders for you.

### 10.3 Corrected version — folder created explicitly first

```yaml
test-job:
  stage: test
  script:
    - mkdir logs
    - echo "These are my test results" > dlog
    - echo "This log is from $CI_JOB_STAGE" >> logs/dlog
  artifacts:
    paths:
      - logs/
    expire_in: 1 week
```
Commit message used: `Added user defined logging folder`, then `Added artifacts`.

Key points explained in the video:
- `paths:` tells GitLab which files/folders to zip up and attach to the job as a downloadable artifact — you give it a **relative path** from the project root (e.g. `logs/` or `builds/`).
- The **`>` operator creates/overwrites** a file; the **`>>` operator appends** to an existing file — used deliberately here (`>` for the first write, `>>` for the second write into the same file so both lines survive).
- **The folder in `paths:` must already exist on disk before the job ends** — always run `mkdir <folder-name>` (or `mkdir -p <folder-name>`) as an earlier `script` line if you're inventing a custom folder name. This is only needed for your own custom folder names — it does **not** apply if you're just referencing GitLab's own default job-artifact behavior.
- `expire_in:` avoids indefinitely accumulating storage — set a sensible TTL (e.g., `1 week`, `30 days`) instead of relying on the default retention forever. The video deliberately set `expire_in: 1 week` so old debug logs get cleaned up automatically.
- **Scope artifacts to only the job/stage that actually needs them.** A common mistake called out in the video: people attach `artifacts:` to the *entire pipeline* (or to jobs like `push` that don't need it), so the `push` job's irrelevant logs also get archived — wasteful. Attach artifacts only where they add value (e.g., the `test` or `deploy` job).
- **Downloading:** go to **Build → Jobs → (the job that produced the artifact) → Download** (top-right button). GitLab bundles it as `artifacts.zip` alongside a `metadata.gz` file it generates automatically. Opening the zip shows your `logs/dlog` file containing the exact text you echoed from your pipeline — proof that pipeline output was successfully captured, versioned, and made shareable with the team.

---

## 11. Runners (SaaS / Instance vs Self-hosted / Project)

> **Runners are the processes that actually pick up and execute your CI/CD jobs.** This is GitLab's equivalent of a Jenkins "agent/node."

### 11.1 Instance Runners (a.k.a. "SaaS Runners" / Shared Runners)
- GitLab.com provides **100+ shared servers worldwide** ("gitlab-shared-runners-manager...") that are **free to use out of the box** for any project — no setup required.
- Visible under `Settings → CI/CD → Runners`.
- Green dot = runner is online/active; check the "last contact" timestamp — stale runners (e.g., no activity for 3 months) may be flaky.
- Great for demos, learning, and light workloads, but you don't control the hardware/OS/tooling on them.

### 11.2 Project (Self-hosted) Runners
You register your own machine (a VM, EC2 instance, on-prem server, or your laptop) as a dedicated runner — giving you full control over installed tools, resource limits, and network access (e.g., to reach a private VPC or on-prem database).

#### Step-by-step setup (as demonstrated on an AWS EC2 Ubuntu instance):

**Step 0 — Provision the machine** (example used: AWS EC2, Ubuntu, x86, t2.micro, security group open for SSH/HTTPS as needed).

**Step 1 — Register a new runner in GitLab**
`Settings → CI/CD → Runners → New project runner`
- Add **tags** (e.g., `dev`) — tags act like Jenkins agent "labels": any job whose YAML specifies `tags: [dev]` will only run on a runner registered with that same tag.
- Choose **not** to use a description (optional) and leave timeout as default.
- Click **Create runner** — GitLab shows you the install & registration commands for your OS/architecture.

**Step 2 — Install the GitLab Runner binary on the machine**

GitLab's UI (`Settings → CI/CD → Runners → New project runner → select OS/architecture`) generates the exact install commands for you. General shape (Linux, x86_64/amd64, as used in the video):
```bash
# 1. Download the binary matching your CPU architecture
curl -L "https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-amd64" -o /usr/local/bin/gitlab-runner

# 2. Give it execute permission
sudo chmod +x /usr/local/bin/gitlab-runner

# 3. Create a dedicated Linux user for the runner (do NOT run jobs as root)
sudo useradd --comment 'GitLab Runner' --create-home gitlab-runner --shell /bin/bash

# 4. Install gitlab-runner as a system service running under that user
sudo gitlab-runner install --user=gitlab-runner --working-directory=/home/gitlab-runner

# 5. Start the service
sudo gitlab-runner start
```
Check status:
```bash
sudo gitlab-runner status
systemctl status gitlab-runner
```
Expected output: `gitlab-runner: Service is running!` / `active (running)`.

**Step 3 — Register the runner against your project**
```bash
sudo gitlab-runner register
```
Copy-paste the full one-line registration command GitLab shows you (it embeds the token), or answer the interactive prompts one by one exactly as shown in the video:

```
Enter the GitLab instance URL (for example, https://gitlab.com/):
> https://gitlab.com/

Verifying runner... is valid          responded_to = OK

Enter a name for the runner. This is stored only in the local config.toml file:
> vivek

Enter an executor: docker, docker-windows, docker+machine, kubernetes, custom, parallels, shell, ssh, virtualbox:
> shell

Runner registered successfully. Feel free to start it, but if it's running already the config should be automatically reloaded!
```
- **Executor** decides *how* jobs actually run. `shell` runs the job's script commands directly on the host machine's shell (simplest — used in the video). Other options: `docker` (each job runs inside a fresh container), `kubernetes`, `virtualbox`, `ssh`, `custom`.
- If the runner was already running, no manual restart is needed — the config auto-reloads. If not:
  ```bash
  sudo gitlab-runner run
  ```

Once registered, the runner shows as **online** (green dot, "last contact: a few seconds ago") in `Settings → CI/CD → Runners`, and jobs whose `tags:` match will be picked up automatically.

### 11.3 Enabling the runner for a specific project (a real "stuck pipeline" fix)
By default a newly-created **project runner** may show up in the Runners list but still not be *enabled/assigned* to the exact project whose pipeline you're trying to run. Symptom: the pipeline sits in **"Pending"** or **"Stuck"** forever, and clicking into it shows one of these reasons:
- *"There are no active runners online"*
- *"No runner for the protected branch"*
- *"No runners that match all of the tags"*

**Fix demonstrated:**
`Settings → CI/CD → Runners → (open your project runner) → toggle "Enable for this project" / "Runner is dedicated to this project"` — once enabled, re-run the pipeline and the stuck state clears.

### 11.4 Tags — matching jobs to runners
```yaml
build-job:
  stage: build
  tags:
    - dev          # this job will ONLY run on a runner registered with the "dev" tag
  script:
    - docker build -ht .
```
This is the direct equivalent of Jenkins agent **labels**: whatever `tags:` you put in a runner's registration, only jobs listing that same tag get scheduled onto it. If no runner exists with a matching tag, the job gets stuck with *"This job is stuck because you don't have any active runners that can run this job."*

### 11.5 Real-time troubleshooting encountered while setting up the self-hosted runner

**Problem A — Runner logs itself out after every single job, breaking subsequent pipeline runs.**

Diagnosis:
```bash
cd /home/gitlab-runner   # or: cd ~/ (the gitlab-runner user's home)
ls -a
# → reveals a hidden file: .bash_logout
```
Inspecting it:
```bash
cat .bash_logout
```
It contained a default Ubuntu snippet that clears the terminal and effectively ends the session "when leaving the console, to increase privacy" — which was killing the runner's active session after each build. **Fix:**
```bash
vim .bash_logout
# comment out (or delete) the "clear" line inside it, then save & quit (:wq)
```
Then restart/re-run the runner and re-trigger the pipeline — the forced logout stops happening.

**Problem B — `docker: permission denied while trying to connect to the Docker daemon socket`**

The dedicated `gitlab-runner` Linux user (created during install) is not a member of the `docker` group, so it cannot talk to `/var/run/docker.sock`.
```bash
sudo usermod -aG docker gitlab-runner   # add the gitlab-runner user to the docker group
cat /etc/group | grep docker            # verify gitlab-runner now appears in the docker group's member list
sudo systemctl restart docker           # restart the Docker daemon
sudo gitlab-runner restart              # restart the runner service so it picks up the new group membership
```
> Note: the fix targets the **`gitlab-runner`** OS user specifically — **not** your default cloud login user (e.g. `ubuntu` on AWS EC2). It's easy to mistakenly add permissions to the wrong user and wonder why nothing changed.

If it still doesn't take effect, a full reboot forces the new group membership to apply everywhere:
```bash
sudo reboot
```

---

## 12. Hands-on: End-to-End Deployment Pipeline

Full walkthrough replicated from the tutorial, using a small Node.js application (a Dockerized app already running on port `8000`) that gets **cloned, built, tested, pushed to Docker Hub, and deployed** — all through GitLab CI/CD, on the same self-hosted EC2 + runner set up in Section 11.

### 12.1 Clone the sample project locally on the runner's instance

```bash
git clone <your-nodejs-project-git-url>
cd <project-folder>          # e.g., cd cicd-node
ls                            # confirm a Dockerfile is present, exposing port 8000
```

### 12.2 Plan the stages out loud (as done in the video) before writing YAML
1. **Build** the project (Docker image).
2. **Test** the project.
3. **Push** the image to Docker Hub.
4. **Deploy** the project (via `docker compose`).

### 12.3 Write `.gitlab-ci.yml` for this project, built up incrementally

**Build job:**
```yaml
stages:
  - build
  - test
  - push
  - deploy

build-job:
  stage: build
  tags:
    - dev
  script:
    - docker build -ht nodeapp:latest .
```

**Test job** (kept intentionally simple in the video — you can add real test commands here):
```yaml
test-job:
  stage: test
  tags:
    - dev
  script:
    - echo "Testing the Docker build"
```

**Push job — the important part:**
```yaml
push-job:
  stage: push
  tags:
    - dev
  script:
    - docker login -u $DOCKER_HUB_USER -p $DOCKER_HUB_PASS
    - docker tag nodeapp:latest $DOCKER_HUB_USER/nodeapp:latest
    - docker push $DOCKER_HUB_USER/nodeapp:latest
```
Note the pattern: **old image name → new image name**, where the new name is `$DOCKER_HUB_USER/<image>:<tag>` — this is standard Docker tagging convention required before any `docker push` to Docker Hub will work.

**Deploy job — using the project's existing `docker-compose.yaml`:**

First, check the project's `docker-compose.yaml` — make sure the `image:` line references only the base image name (the video had it mistakenly pinned to an older/wrong tag and had to trim it back down to the correct image reference), and confirm Docker is installed on the runner machine:
```bash
docker --version
docker compose version
```
Then:
```yaml
deploy-job:
  stage: deploy
  tags:
    - dev
  script:
    - docker compose up -d
```

### 12.4 Full, final `.gitlab-ci.yml` for this project

```yaml
stages:
  - build
  - test
  - push
  - deploy

build-job:
  stage: build
  tags:
    - dev
  script:
    - docker build -ht nodeapp:latest .

test-job:
  stage: test
  tags:
    - dev
  script:
    - echo "Testing the Docker build"

push-job:
  stage: push
  tags:
    - dev
  script:
    - docker login -u $DOCKER_HUB_USER -p $DOCKER_HUB_PASS
    - docker tag nodeapp:latest $DOCKER_HUB_USER/nodeapp:latest
    - docker push $DOCKER_HUB_USER/nodeapp:latest

deploy-job:
  stage: deploy
  tags:
    - dev
  script:
    - docker compose up -d
```

### 12.5 Commit and push this file using plain Git (not the Web UI this time)

Because this project was cloned onto the EC2 instance directly (not edited via GitLab's browser IDE), the file was created/edited locally and pushed with standard Git commands:
```bash
git status
# On branch master
# Untracked/modified files: .gitlab-ci.yml, docker-compose.yaml

git add .gitlab-ci.yml docker-compose.yaml
git commit -m "Added CICD and Docker changes"
git push origin master
```

### 12.6 Installing Docker + Docker Compose on the runner machine (prerequisite, done proactively)

To rule out "is Docker even installed" as a source of pipeline failures, Docker was explicitly (re)installed on the EC2 instance hosting the self-hosted runner:
```bash
sudo apt update
sudo apt install docker.io docker-compose -y
```
> **Important distinction called out in the video:** `docker-compose` (hyphen) is the older, standalone Python-based binary; `docker compose` (space) is the newer Compose V2 plugin bundled with modern Docker installs. If your `.gitlab-ci.yml` calls one but only the other is installed on the runner, you'll get:
> ```
> docker-compose: command not found
> ```
> **Fix:** update the `deploy-job` script line to match whichever is actually installed — the video ultimately standardized on:
> ```yaml
> script:
>   - docker compose up -d
> ```
> Always verify first:
> ```bash
> docker compose version     # v2 plugin (space)
> docker-compose --version   # legacy standalone (hyphen)
> ```

### 12.7 Resolving a Git conflict encountered while iterating on the file

After several rounds of editing `.gitlab-ci.yml` both locally (via terminal) and once via the GitLab web UI/Pipeline Editor on the same `master` branch, a conflict appeared on push:
```bash
git pull origin master
# CONFLICT (content): Merge conflict in .gitlab-ci.yml
```
Resolution steps used:
```bash
# open .gitlab-ci.yml, manually keep the correct version of the conflicting lines,
# removing the <<<<<<<, =======, >>>>>>> conflict markers

git add .gitlab-ci.yml
git commit -m "Resolved merge conflict in .gitlab-ci.yml"
git push origin master
```
> This is a **plain Git conflict**, not a GitLab-specific problem — it happens whenever two divergent commit histories exist for the same branch (in this case: one from the terminal, one from the browser-based editor).

This project ran through the *exact* same class of real errors documented in [Section 13](#13-real-errors-faced--how-they-were-fixed) below (stuck pipeline from a disabled runner, Docker permission denied, TTY login error, missing project-level variables, wrong Docker Compose command) before finally completing all four stages successfully.

---

## 13. Real Errors Faced & How They Were Fixed

These are genuine, unscripted debugging moments from the live session — they are *extremely* valuable because they mirror what you'll actually hit in production work.

| # | Exact error / symptom | Root Cause | Fix (exact commands / clicks) |
|---|---|---|---|
| 1 | `Job: build-job config should implement the script, run, and trigger keyword` — also seen as **"script is not allowed"** | An invalid/misspelled keyword was used in the job definition (e.g., `scripts` instead of `script`, or `run` used incorrectly) in `.gitlab-ci.yml` | Fix the exact keyword spelling; use the Pipeline Editor's **Validate** tab (or `CI/CD → Editor → Validate`) which lints the YAML and names the invalid line before you even run the pipeline |
| 2 | Pipeline stuck in **"Pending"** forever, never starts | Symptom of one of three causes GitLab itself lists: *no active runners online*, *no runner for the protected branch*, or *no runners matching the tags*. In this case: the self-hosted **project runner existed but was not enabled/assigned to this specific project** | `Settings → CI/CD → Runners → (open the runner) → enable "Runner is dedicated to this project"` → re-run the pipeline |
| 3 | Runner logs itself out after every job, next pipeline run then fails at "Preparing environment" | A default `.bash_logout` script on the runner's Linux user was clearing the console (and killing the session) after every job | `cd` into the `gitlab-runner` user's home → `ls -a` → find `.bash_logout` → `vim .bash_logout` → comment out the `clear` line → save → restart the runner and re-run |
| 4 | `docker: permission denied while trying to connect to the Docker daemon socket` | The `gitlab-runner` OS user is not a member of the `docker` group, so it cannot access `/var/run/docker.sock` | `sudo usermod -aG docker gitlab-runner` → verify with `cat /etc/group \| grep docker` → `sudo systemctl restart docker` → restart `gitlab-runner` (a `sudo reboot` may be needed if it still doesn't take effect) |
| 5 | Build succeeds even though Docker permission looked broken — confusing intermediate state | The `build` job ran fine because it only needed `docker build`, which had already cached/succeeded before the permission issue surfaced on the *next* job in the chain that also touched Docker | Re-check permissions on the correct OS user (`gitlab-runner`, not your personal cloud login user like `ubuntu`) — a common trap is fixing permissions for the wrong Linux user |
| 6 | `Cannot perform an interactive login from a non TTY device` | Two separate causes seen back to back: (a) `docker login` was effectively being called in a way that expected an interactive terminal, and (b) a **Protected** variable was being used on a **branch that was not marked as Protected** | (a) Always use the non-interactive flag form: `docker login -u $DOCKER_HUB_USER -p $DOCKER_HUB_PASS`; (b) either protect the branch (`Settings → Repository → Protected branches`) to match the variable, or uncheck "Protect variable" on the CI/CD variable so it is exposed to unprotected branches too |
| 7 | Variable prints empty / pipeline can't find `$DOCKER_HUB_USER` or `$DOCKER_HUB_PASS` | The variable was only ever added to a *different* project's CI/CD Settings — variables don't automatically cross over between projects | Go to **the exact project currently failing** → `Settings → CI/CD → Variables → Add variable` and re-declare both there (or promote them to Group-level variables so every project under that Group inherits them) |
| 8 | `docker login` fails with **incorrect username and password** | A literal typo — the instructor's own name was mistyped in the `DOCKER_HUB_USER` variable value (`shbuham` instead of `shubham`) | Open the variable, correct the value, save — then **retry just the failed job** (`push-job` in this case) instead of re-running the whole pipeline, using the **Retry** button on that specific job |
| 9 | `docker-compose: command not found` | The runner machine only had the newer Docker Compose **v2 plugin** (`docker compose`, space) installed — not the legacy standalone `docker-compose` (hyphen) binary the YAML called | Edit `.gitlab-ci.yml`'s `deploy-job` script to use `docker compose up -d` (space) instead of `docker-compose up -d` (hyphen); commit and push again |
| 10 | Merge/rebase conflict when pushing `.gitlab-ci.yml` again | Direct edits were made both from the local terminal (`git push`) and via GitLab's browser Web IDE/Pipeline Editor on the same branch, producing divergent commit histories | `git pull origin master` → manually resolve the `<<<<<<< / ======= / >>>>>>>` conflict markers inside the file → `git add .` → `git commit` → `git push origin master` — a standard Git conflict, unrelated to GitLab specifically |

> **Takeaway repeated throughout the session:** a real DevOps/DevSecOps engineer's job is *not* "write 10 lines of YAML and done" — it's methodically reading error messages, isolating whether the problem is (a) YAML syntax, (b) runner availability, (c) permissions, (d) variable scope, or (e) plain Git mechanics, and fixing them one at a time.

---

## 14. DevSecOps — The Bigger Picture

DevSecOps = **DevOps + Security baked into every stage of the pipeline**, instead of security being a separate, late-stage gate.

Extended pipeline example (compared to plain DevOps: Code → Build → Test → Deploy):

```
Code → Code Quality/SAST Scan → Build → Image Scan → OWASP/DAST Test → Deploy
```

| Stage | Purpose | Common Tools |
|---|---|---|
| **Code Quality Analysis (SAST)** | Static scan of *your source code* for bugs, code smells, and vulnerabilities like SQL injection before it's even built | SonarQube, GitLab's built-in SAST |
| **Image Scanning** | Scan the built **Docker image** for known CVEs in its base image/layers | Trivy, **Docker Scout** |
| **OWASP / DAST checks** | Dynamic testing of the *running* web application against the OWASP Top 10 vulnerability categories | OWASP ZAP, GitLab DAST |

**OWASP** = **Open Worldwide Application Security Project** (the instructor wasn't sure of the exact expansion in the video — this is the correct, current, official name; it was historically called "Open Web Application Security Project," but the foundation rebranded to "Worldwide" in 2023 to reflect its global, non-web-only scope). It is a nonprofit foundation that publishes the widely-used **OWASP Top 10** list of critical web application security risks (e.g., broken access control, injection, security misconfiguration), and maintains free tools like OWASP ZAP for security testing.

**Why it matters for a DevOps engineer today:** as pipelines get more automated, *you* are increasingly the one responsible for embedding these security checks directly into `.gitlab-ci.yml`, not a separate "security team" working in isolation after the fact. GitLab bundles many of these scanners natively as templates you can `include:` into your pipeline (see [GitLab Application Security docs](https://docs.gitlab.com/user/application_security/)).

---

## 15. GitLab CI/CD YAML Cheat Sheet

A quick-reference of the most common top-level and job-level keywords (see the [official keyword reference](https://docs.gitlab.com/ci/yaml/) for the full list):

| Keyword | Level | Purpose |
|---|---|---|
| `stages` | top-level | Ordered list of all stage names in the pipeline |
| `stage` | job-level | Which stage (from `stages`) this job belongs to |
| `script` | job-level | Shell commands the job executes (single line or list) |
| `before_script` / `after_script` | job or global | Commands run before/after the main `script`, useful for setup/teardown |
| `tags` | job-level | Restrict which runner(s) — by tag — can pick up this job |
| `variables` | global, job, or group/project settings | Define reusable key-value pairs |
| `artifacts.paths` | job-level | Files/folders to preserve after the job |
| `artifacts.expire_in` | job-level | TTL for stored artifacts (e.g., `1 week`, `30 days`) |
| `rules` / `only` / `except` | job-level | Conditionally control when a job runs (branch, tag, MR event, variable value, etc.) — `rules` is the modern, recommended replacement for the older `only`/`except` |
| `needs` | job-level | Lets a job start as soon as its specific dependency jobs finish, instead of waiting for the whole previous stage (enables a DAG instead of strict linear stages) |
| `image` | job-level or global | Docker image to run the job's container in (when using the `docker` executor) |
| `environment` | job-level | Tags a job as deploying to a named environment (e.g., `production`), enabling GitLab's Environments/Deployments dashboard |
| `include` | top-level | Pull in reusable pipeline templates/snippets from other files or GitLab's built-in security templates |
| `parallel` | job-level | Run multiple instances of the same job in parallel (matrix-style) |

---

## 16. GitLab Duo — AI in GitLab (2026 Update)

*(This section covers developments after the original tutorial was recorded — GitLab's AI features evolve quickly, so treat this as a snapshot as of mid/late 2026.)*

- GitLab's AI suite is branded **GitLab Duo** — positioned as an AI layer across the *entire* DevSecOps lifecycle (planning, coding, code review, testing, security, and deployment), not just an inline code-completion tool like GitHub Copilot.
- In January 2026, GitLab announced **General Availability of the "GitLab Duo Agent Platform"** — an orchestration layer for multiple specialized AI agents (e.g., a Planner agent, a Security Analyst agent) that can take multi-step actions across your codebase, CI/CD pipelines, and issue tracker, available to Premium/Ultimate customers on GitLab.com and self-managed instances.
- Duo ties into a feature called **GitLab Orbit**, described as a continuously-updated "lifecycle context graph" connecting code, merge requests, pipelines, and deployments so agents can reason across the whole project rather than just the files in front of them.
- Pricing (approximate, subject to change): base **Duo Core** AI features are bundled into the **Premium** tier; **Duo Pro** is a paid add-on for deeper coding assistance; heavier **agentic** usage is billed via usage-based **GitLab Credits**.
- Practical takeaway for a learner: don't rely purely on old tutorials for the AI feature names/pricing — always check the current [GitLab Duo docs](https://docs.gitlab.com/user/gitlab_duo/) since this area changes monthly.

---

## 17. Further Reading / Official Links

- GitLab CI/CD YAML keyword reference: https://docs.gitlab.com/ci/yaml/
- GitLab CI/CD variables (predefined + custom): https://docs.gitlab.com/ci/variables/
- GitLab Runner installation docs: https://docs.gitlab.com/runner/install/
- GitLab Artifacts docs: https://docs.gitlab.com/ci/jobs/job_artifacts/
- GitLab Application Security (SAST/DAST/Container Scanning): https://docs.gitlab.com/user/application_security/
- OWASP Foundation (Top 10, ZAP, etc.): https://owasp.org/
- GitLab Duo documentation: https://docs.gitlab.com/user/gitlab_duo/

---

### How to use this file for revision
1. Skim Sections 1–7 to re-anchor the *conceptual* differences (GitLab vs GitHub, Groups vs Projects).
2. Rebuild the pipeline in [Section 12](#12-hands-on-end-to-end-deployment-pipeline) from memory on a fresh EC2/VM, without copy-pasting.
3. Deliberately break something (wrong tag, unprotected variable, wrong docker-compose command) and use [Section 13](#13-real-errors-faced--how-they-were-fixed) to practice diagnosing it *before* looking at the fix.
4. Once comfortable, extend the pipeline with a real `rules:`/`needs:` based DAG and one DevSecOps scanning stage from [Section 14](#14-devsecops--the-bigger-picture).
