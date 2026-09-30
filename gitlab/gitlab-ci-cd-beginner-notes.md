# GitLab CI/CD – Complete Beginner Notes

> Detailed notes from a Hindi/English tutorial "How to Start Working with GitLab CI/CD". Every step, command and YAML file shown in the video is reproduced below, with a few clarifications and modern-GitLab tips added (marked **💡 Note**).

**Prerequisites:** basic knowledge of **Git** and **GitHub** (clone, add, commit, push, branches, remotes).

---

## Table of Contents

1. [What is GitLab (CI/CD tool)?](#1-what-is-gitlab-cicd-tool)
2. [CI/CD in short](#2-cicd-in-short)
3. [Setting up GitLab for the first time](#3-setting-up-gitlab-for-the-first-time)
4. [Dashboard overview (GitLab vs GitHub)](#4-dashboard-overview-gitlab-vs-github)
5. [Your first pipeline – `.gitlab-ci.yml`](#5-your-first-pipeline--gitlab-ciyml)
6. [How it works behind the scenes (Runners)](#6-how-it-works-behind-the-scenes-runners)
7. [Multiple jobs and `stages`](#7-multiple-jobs-and-stages)
8. [Failure handling (negative test)](#8-failure-handling-negative-test)
9. [`before_script` and `after_script`](#9-before_script-and-after_script)
10. [Running a Bash script from the pipeline](#10-running-a-bash-script-from-the-pipeline)
11. [Artifacts (preserving files)](#11-artifacts-preserving-files)
12. [Auto-run on every commit](#12-auto-run-on-every-commit)
13. [Environment (CI/CD) variables](#13-environment-cicd-variables)
14. [Email notifications](#14-email-notifications)
15. [Manual runs, retry and scheduling](#15-manual-runs-retry-and-scheduling)
16. [Manual deployment with `when: manual`](#16-manual-deployment-with-when-manual)
17. [Predefined variables](#17-predefined-variables)
18. [Working with GitHub → import a repo into GitLab](#18-working-with-github--import-a-repo-into-gitlab)
19. [Choosing a Docker image per job](#19-choosing-a-docker-image-per-job)
20. [Local project → GitLab (static website + GitLab Pages)](#20-local-project--gitlab-static-website--gitlab-pages)
21. [Troubleshooting cheat sheet](#21-troubleshooting-cheat-sheet)
22. [Practice project ideas](#22-practice-project-ideas)
23. [Quick reference / cheat sheet](#23-quick-reference--cheat-sheet)

---

## 1. What is GitLab (CI/CD tool)?

- **Web-based / cloud-based** – open `gitlab.com` in a browser; no installation or server management (unlike **Jenkins**, which you install and maintain yourself).
- A **self-managed** option also exists (install GitLab on your own server), but `gitlab.com` is easier and future-proof, so the course uses it.
- It is not just CI/CD. In one tool you get:
  - **CI/CD pipelines** (main reason we learn it)
  - **Source code management** (Git repositories, branches, merge requests – same concepts as GitHub)
  - **Collaboration & project management** (teams, issues, boards)
  - **Monitoring, security, email notifications**
- It automates parts of the **software development life cycle**: **Build → Test → Deploy** (hence "DevOps life-cycle tool").

---

## 2. CI/CD in short

| Term | Meaning | Typical stages |
|---|---|---|
| **CI** – Continuous Integration | Automatically build, test and merge code changes | Build → Test → Merge |
| **CD** – Continuous Delivery | Automatically release a ready-to-ship package to a repo/registry (a human decides when to go live) | Package/release |
| **CD** – Continuous Deployment | Automatically deploy every passing change to **production** | Deploy to prod |

**Delivery vs Deployment:** in *delivery* the software is ready to hand to the customer / go live; in *deployment* it actually goes live automatically.

---

## 3. Setting up GitLab for the first time

### 3.1 Free tier (what the video says + current info)

- Go to **https://gitlab.com** (redirects to `about.gitlab.com`).
- Free plan: **$0/month, no credit card required**.
- Limits mentioned in the video: **5 GB storage**, **100 GB transfer/month**, **400 compute minutes/month**, **5 users per top-level group**.
- **Compute minutes** = total time your pipelines/jobs spend running on GitLab's shared runners each month. 400 is plenty for practice.

> **💡 Note (verified from current GitLab docs/pricing pages):**
> - The **400 compute minutes/month** and **5-user limit for private top-level groups** are still in force. Personal namespaces and public groups are not subject to the user limit.
> - Storage numbers differ between sources (5 GiB in older material, ~10 GiB quoted on newer pages). Check **https://about.gitlab.com/pricing/** for the exact current number.
> - GitLab announced (June 2026) it will enforce the user limit on all remaining Free private namespaces from **August 15, 2026** – keep private groups ≤ 5 users.
> - Paid tiers: Premium (~$29/user/month) and Ultimate offer far more compute minutes.

### 3.2 Create the account (step by step)

1. Open `gitlab.com` → **Sign in / Register**. You can sign in with **GitHub** or Google credentials.
2. **Verify email** and **phone number** (validation is required for using shared runners on free accounts).
3. Refresh; the welcome questionnaire appears:
   - Role → e.g. *DevOps Engineer*
   - Reason → *"I want to try GitLab to see if it's worth switching to"*
   - Who will use it → *Just me*
   - Choose **Create a new project** (not Join a project).
4. Enter **Group name** (e.g. `testing`) and **Project name** (e.g. `test`) → **Create project**.
5. A "Congratulations on creating your project" page offers *Invite colleagues* – **Cancel/skip** for now (used for team collaboration).

### 3.3 Personalise the UI (optional)

Profile picture (top-left) → **Preferences**:
- **Appearance** → Color mode: *Dark*
- **Navigation theme:** e.g. *Green*
- **Syntax highlighting theme:** your choice (preview shown) → **Save changes**

Your projects appear under the GitLab logo → **Projects**.

---

## 4. Dashboard overview (GitLab vs GitHub)

GitLab is essentially an *advanced level of Git hosting* – anything you did on GitHub you can do here:

| Task | GitHub | GitLab |
|---|---|---|
| Repo home | Code tab, README | Project overview, README |
| Add files / branches | ✔ | ✔ (+ button, Branches) |
| Clone URL | Code → HTTPS/SSH | **Code** button → HTTPS/SSH URL |
| Fork, branch, push, pull | ✔ | ✔ |
| CI/CD | GitHub Actions | **Built-in pipelines** (`.gitlab-ci.yml`) |

Extra on GitLab: build, test, deploy automation on the **same platform**.

---

## 5. Your first pipeline – `.gitlab-ci.yml`

A pipeline is defined in a YAML file in the repo root, named **exactly**:

```
.gitlab-ci.yml
```

(`.gitlab` + `-ci` + `.yml`; it starts with a dot. Similar to a Dockerfile or a Jenkinsfile.)

### Steps

1. In the project click **+ → New file**.
2. Name it `.gitlab-ci.yml` (GitLab also offers *templates* – we write from scratch to understand).
3. Add content:

```yaml
build:
  script:
    - echo "First step"
    - echo "Second step"
```

4. **Commit changes** (branch `main`, edit the commit message if you like).

### Key concepts

- `build:` is a **job name**. It is *not* a reserved word – you may name it `building`, `compile`, anything.
- `script:` is the list of shell commands the job runs. A job can have multiple steps (each list item starts with `-`).
- The editor **auto-indents** and validates YAML.
- **Validation:** if you make a mistake (e.g. type `script` as `scripts`), GitLab shows **"CI configuration is invalid"** immediately – handy for catching errors.

### Auto-trigger

As soon as you commit `.gitlab-ci.yml`, a pipeline **starts automatically**. Click the pipeline status icon (or **Build → Pipelines**) to see it.

---

## 6. How it works behind the scenes (Runners)

Click the job (e.g. `build`) to see its **logs** (like Jenkins console output):

```
Running with gitlab-runner ...
Preparing the "docker+machine" executor
Using Docker executor with image ruby:3.1 ...
Getting source from Git repository
Executing "step_script" stage of the job script
$ echo "First step"
First step
$ echo "Second step"
Second step
Job succeeded
```

Flow:

1. You commit → GitLab triggers the pipeline.
2. A **GitLab Runner** is assigned. A runner is a machine/instance (part of GitLab) responsible for running your jobs. On the free tier they are **shared**.
3. Runner starts a **Docker container** (default image: `ruby:3.1`, lightweight) – the *environment* where the job runs.
4. It **fetches your repo source** into the container.
5. It runs the `script` commands in order and reports success/failure.

> **💡 Note:** Because runners and the platform are shared and you're on free tier, pipelines are slower than Jenkins on your own server. You can register dedicated/self-hosted runners to speed things up.

---

## 7. Multiple jobs and `stages`

### 7.1 Multiple jobs (they run in parallel by default!)

Open **Pipeline editor** (Build → Pipeline editor) – VS Code-like editor with auto-suggestions – or edit the file directly.

```yaml
build:
  script:
    - echo "Building"

test:
  script:
    - echo "Testing"

deploy:
  script:
    - echo "Deploying"
```

Commit → all three jobs run **in parallel**. But we want *Build → Test → Deploy* in order.

### 7.2 Enforce sequence with `stages`

```yaml
stages:
  - build
  - test
  - deploy

build:
  stage: build
  script:
    - echo "Building"

test:
  stage: test
  script:
    - echo "Testing"

deploy:
  stage: deploy
  script:
    - echo "Deploying"
```

- `stages:` defines the **order**.
- Each job gets `stage: <name>`.
- Jobs of the same stage run in parallel; the next stage starts only after the previous one **succeeds**.
- To see logs of one job: click its status icon; use the dropdown on the right of the log page to switch between build/test/deploy jobs.
- **Overall history:** left menu **Build → Pipelines** shows all runs (green = pass, red = fail) and a **Run pipeline** button at top-right.

---

## 8. Failure handling (negative test)

Break the build job on purpose (`echos` is not a command):

```yaml
build:
  stage: build
  script:
    - echos "Building"      # wrong command -> job fails
```

Result: `build` **fails**, so `test` and `deploy` are **skipped** ("Skipped" status). GitLab handles it correctly. You can still run skipped jobs manually if you want.

---

## 9. `before_script` and `after_script`

- `before_script` runs **before** each job's `script`.
- `after_script` runs **after** it (even if the script fails).
- Typical use: `before_script` → check environment, install dependencies, update system; `after_script` → clean up files/space.

### Global (applies to ALL jobs) – defined outside jobs

```yaml
stages:
  - build
  - test
  - deploy

before_script:
  - echo "Before script (global)"

after_script:
  - echo "After script (global)"

build:
  stage: build
  script:
    - echo "Building"
```

### Job-specific (applies to ONE job only) – defined inside the job

```yaml
build:
  stage: build
  before_script:
    - echo "Before build step (only for build job)"
  script:
    - echo "Building"
  after_script:
    - echo "Cleaning up (only for build job)"
```

Logs show: `before_script` → `script` → `after_script` for each job.

---

## 10. Running a Bash script from the pipeline

### 10.1 Create the script in the repo

New file `basic.sh`:

```bash
#!/bin/bash
echo "This is from bash script"
touch myfile.txt
echo "sample text" > myfile.txt
echo "This is end of the script"
```

Commit with message like *"Adding new bash script"*.

### 10.2 Call it from `.gitlab-ci.yml`

Remove earlier jobs to save compute minutes and use:

```yaml
execute-script:
  script:
    - bash ./basic.sh
```

- `./` = the current directory (repo root inside the container) where `basic.sh` was checked out.
- Logs show the three echo lines, proving the whole script ran.
- After the job finishes, the created `myfile.txt` **disappears** (container is destroyed). To keep it → **artifacts**.

---

## 11. Artifacts (preserving files)

Artifacts = files produced by a job that GitLab stores so you can **download** them or pass them to later jobs (e.g. a built `.jar` for deployment).

### First (failing) attempt – learn from the mistake

```yaml
execute-script:
  script:
    - mkdir my-folder
    - cd my-folder
    - bash basic.sh        # ❌ basic.sh is NOT inside my-folder
    - touch newfile
  artifacts:
    paths:
      - ./my-folder
```

This fails: it's a **conceptual error**, not a syntax error – after `cd my-folder` the script `basic.sh` isn't there (it lives in the repo root).

### Corrected version

```yaml
execute-script:
  script:
    - mkdir my-folder
    - cp basic.sh my-folder       # copy script into the folder
    - cd my-folder
    - bash basic.sh
    - touch newfile
  artifacts:
    paths:
      - ./my-folder               # multiple paths can be listed
```

Optional settings (defaults shown in GitLab's suggestions):

```yaml
  artifacts:
    untracked: false
    when: on_success       # on_success | on_failure | always
    expire_in: 30 days     # how long stored
    paths:
      - my-folder
```

### Getting the artifact

Job page → right side **"Job artifacts"**: **Keep / Download / Browse**.
- **Download** → `artifacts.zip`.
- **Browse** → shows `my-folder/` containing `basic.sh`, `myfile.txt`, `newfile` (empty). Open `myfile.txt` → contains `sample text` ✅.

> Artifacts are created only if the job **succeeds** (with `when: on_success`).

---

## 12. Auto-run on every commit

The pipeline runs automatically whenever:

- `.gitlab-ci.yml` is created/edited, **or**
- **any file in the repo** changes (e.g. edit `basic.sh` and add a line `echo "Adding new line"`).

Commit → pipeline starts on its own → the log shows the new line. (You can control/disable this with rules, but auto-run is the default and is the essence of CI.)

---

## 13. Environment (CI/CD) variables

Use variables for values/secrets so you don't hard-code them in YAML.

### Create variables

Project → **Settings → CI/CD → Variables → Add variable**.

| Field | Meaning |
|---|---|
| Type | Variable or File |
| Environments | Which environment it applies to (default = all) |
| Visibility | **Visible** (shown in logs), **Masked** (hidden as `[MASKED]`), **Masked and hidden** |
| Key / Value | Name and value |

Example variables created:

| Key | Value | Visibility |
|---|---|---|
| `name` | `gitlab` | Visible |
| `pass` | `testtest` (min **8 characters** required for masking) | Masked |

### Use them in a job (with `$`)

```yaml
print-variables:
  script:
    - echo "Name is $name"
    - echo "Password is $pass"
```

Log output:

```
Name is gitlab
Password is [MASKED]
```

> **💡 Note:** Never print real secrets; masking is a safety net, not a licence to echo them. Use **Protected** variables for protected branches/tags only.

---

## 14. Email notifications

GitLab emails you on pipeline status automatically:

1. Make a job fail on purpose (e.g. `echos "..."`) and commit.
2. Inbox receives **"Pipeline #… has failed"** with commit details and link – shows exactly which commit broke it.
3. Fix the mistake (`echo`) and commit.
4. Second email arrives: **"Pipeline has been fixed"**.

So you get notified both on **failure** and when it's **fixed**. (Notification levels can be changed in profile → Notifications.)

---

## 15. Manual runs, retry and scheduling

### 15.1 Run manually

**Build → Pipelines → Run pipeline** (top-right), choose branch → run.
(Useful when nothing changed but you want to run it again.)

### 15.2 Retry a failed job

In the pipeline view, a failed job has a **Retry** button (circular arrow icon).

### 15.3 Schedule pipelines

Use when you don't want to sit at the screen 24×7, e.g. *"run every Sunday"* or nightly.

**Build → Pipeline schedules → New schedule**

- **Interval pattern:** presets – Every day (2 AM), Every week (Sunday 2 AM), Every month (day 11, 2 AM) – or **Custom** using **cron syntax**.
- **Cron examples**
  - `0 19 * * *` → every day at 7 PM
  - `* * 3 6 *` → every minute on 3rd June
  - `0 2 * * 0` → every Sunday at 2 AM
- **Cron timezone:** select yours.
- **Target branch/tag:** e.g. `main`.
- **Description:** e.g. "Custom schedule".
- Save → the list shows **"Next run in 21 hours"**, so the pipeline runs automatically.

Cron format reminder:

```
┌───── minute (0-59)
│ ┌───── hour (0-23)
│ │ ┌───── day of month (1-31)
│ │ │ ┌───── month (1-12)
│ │ │ │ ┌───── day of week (0-6, Sun=0)
* * * * *
```

---

## 16. Manual deployment with `when: manual`

Goal: build and test on **every** change, but deploy only when *you* approve.

```yaml
stages:
  - build
  - test
  - deploy

build:
  stage: build
  script:
    - echo "Building"

test:
  stage: test
  script:
    - echo "Testing"

deploy:
  stage: deploy
  script:
    - echo "Deploying"
  when: manual
```

Result: build and test pass; the deploy job shows a **▶ Play / Run** button and **does not run** until you click it.

> **💡 Note:** In older GitLab, manual jobs are "allowed to fail" by default so the pipeline can appear *passed* while deploy is still waiting. Add `allow_failure: false` to make the pipeline **block** on the manual job.
>
> ```yaml
> deploy:
>   stage: deploy
>   script: [ "echo Deploying" ]
>   when: manual
>   allow_failure: false
> ```

---

## 17. Predefined variables

GitLab provides many ready-made variables (no need to define them) with info about the commit, project, pipeline, job and runner. Full list: GitLab Docs → *CI/CD → Variables → Predefined variables*.

Common ones:

| Variable | Meaning |
|---|---|
| `$CI_COMMIT_AUTHOR` | Author of the commit ("Name <email>") |
| `$CI_COMMIT_BRANCH` | Branch name |
| `$CI_COMMIT_MESSAGE` | Full commit message |
| `$CI_COMMIT_SHA` | Commit hash |
| `$CI_JOB_ID` | ID of current job |
| `$CI_PIPELINE_ID` | ID of current pipeline |
| `$CI_PROJECT_NAME` | Project name |
| `$CI_PROJECT_DIR` | Directory where the repo is cloned |
| `$GITLAB_USER_NAME` / `$GITLAB_USER_EMAIL` | User who triggered the job |

Example:

```yaml
show-info:
  script:
    - echo "Commit author is $CI_COMMIT_AUTHOR"
    - echo "Branch is $CI_COMMIT_BRANCH"
    - echo "Job ID is $CI_JOB_ID"
    - echo "Triggered by $GITLAB_USER_NAME ($GITLAB_USER_EMAIL)"
```

The log prints the actual values (username, email, etc.).

---

## 18. Working with GitHub → import a repo into GitLab

Scenario: source code already lives on **GitHub** (e.g. a small Python program `test.py`).

### 18.1 Import

1. GitLab → **+ → New project/repository → Import project**.
2. Choose **GitHub** → **Authorize** (log in with GitHub credentials).
3. GitLab lists all your GitHub repos with **Import** buttons (import one or all).
4. Click **Import** for the desired repo → wait for *Complete*.
5. Back on the home page: a **new project** with your files has appeared.

(Other sources are supported too: Bitbucket, Gitea, manifest file, repo by URL, etc.)

### 18.2 Add a pipeline file – first attempt (fails)

New file `.gitlab-ci.yml`:

```yaml
build:
  script:
    - python test.py
```

Result: **failed** – `python: command not found`. The default image (Ruby) has no Python.

### 18.3 Fix – specify an image (see next section)

---

## 19. Choosing a Docker image per job

Use `image:` to pick the environment/container the job runs in.

```yaml
build:
  image: python
  script:
    - python test.py
```

- You may pin a version: `image: python:3.12`, `image: node:20` (great when your app was built for a specific version).
- Images are pulled from Docker Hub by default.
- You can also set a **global default image** at the top of the file so it applies to all jobs:

```yaml
image: python:3.12

build:
  script:
    - python test.py
```

Now the job passes and the log shows the Python program's output.

---

## 20. Local project → GitLab (static website + GitLab Pages)

Scenario: a simple static website (`index.html` + `styles.css`, e.g. an online résumé) exists **only on your laptop**. Deploy it via GitLab Pages.

### 20.1 Create a blank project on GitLab

1. **New project → Create blank project**.
2. Project name: `my-static-web-page`.
3. Visibility: **Private** (for now).
4. ✅ **Initialize repository with a README** – *(the video ticks it; see the note below for a cleaner alternative).*
5. **Create project**.

GitLab shows two ways to add files: (a) *Create/Upload files* (old-school, via browser) or (b) **Git commands** (we use these).

### 20.2 Turn your local folder into a Git repo (VS Code integrated terminal)

Open the folder in VS Code → right-click → **Open in Integrated Terminal**.

```bash
# Is it already a repo?
git status
# fatal: not a git repository

git init
git status                      # now shows the 2 untracked files
git add *
git commit -m "first commit"
git status                      # nothing to commit, working tree clean
```

### 20.3 Connect to GitLab and push

Copy the project's HTTPS URL (**Code → Clone with HTTPS**):

```bash
git remote add origin https://gitlab.com/<your-username>/my-static-web-page.git
git branch -M main
git push -u origin main
```

### 20.4 Authentication problem: `HTTP Basic: Access denied`

GitLab password login over HTTPS is not accepted. Options: **Personal Access Token (PAT)**, a password/SSH key. (GitLab's dashboard warning banner points to the same fix.)

**Create a PAT:**

1. Profile → **Edit profile → Access tokens → Add new token**.
2. Name (e.g. `my-token`), set expiry.
3. Scopes: at minimum **`write_repository`** (push/pull over HTTP) – the video also uses read/write repo access. Use `api` only if you need API access.
4. **Create** and **copy the token immediately** – it disappears when you refresh the page. Save it in a safe place.

**Push again:** when prompted, username = your GitLab username, **password = the token**.

```bash
git push -u origin main
# Username: <your-gitlab-username>
# Password: <paste-token>
```

### 20.5 Error: `You are not allowed to force push code to a protected branch`

Cause: the remote project was initialised with a README, so its `main` history differs from your local `main`, and `main` is a **protected branch** by default (only maintainers can push; force-push disallowed).

**Option A (used in the video):** Settings → **Repository → Protected branches** → expand `main` → enable **Allowed to force push** → push again:

```bash
git push -u origin main --force
```

**Option B (cleaner, no protection changes):** merge the histories instead of force-pushing:

```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

> **💡 Note:** Best practice is to create the GitLab project **without** the README when you already have local code – then a plain `git push -u origin main` works. Re-protect `main` afterwards if you disabled force-push.

After a successful push the two files appear in the GitLab project.

### 20.6 Create the pipeline file (GitLab Pages)

Create `.gitlab-ci.yml` **locally** in the project root (or in the GitLab web editor):

```yaml
image: alpine:latest

pages:
  stage: deploy
  script:
    - mkdir public
    - cp index.html styles.css public/
  artifacts:
    paths:
      - public
  only:
    - main
```

Explanation:

- Job name **must be `pages`** – GitLab recognises it as the special job for GitLab Pages.
- Pages serves whatever is in the **`public`** folder, so we create it and copy the site files in, then preserve it with **artifacts**.
- `image: alpine:latest` – very lightweight Linux image, quick to run.
- `only: main` – job runs only for the `main` branch.

> **💡 Note (modern syntax):** `only:` is legacy; the recommended way is `rules:`. Equivalent modern version:
>
> ```yaml
> image: alpine:latest
>
> pages:
>   stage: deploy
>   script:
>     - mkdir -p public
>     - cp index.html styles.css public/
>   artifacts:
>     paths:
>       - public
>   rules:
>     - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
> ```
>
> Newer GitLab versions (17.x+) also support a `pages: true`/`pages.publish` style keyword and a different Pages UI; if your site doesn't appear, check the Pages docs for your GitLab version.

### 20.7 Push the pipeline file

```bash
git status                       # shows .gitlab-ci.yml untracked
git add .gitlab-ci.yml
git commit -m "Added CI file"
git push
```

The pipeline starts automatically. The `pages` job succeeds, and on the right side you see the artifact – the browsable `public/` folder containing `index.html` and `styles.css`.

### 20.8 Access your website

**Deploy → Pages** → **Access pages** → click the link. Your static site is live over **HTTPS** on a `gitlab.io` URL.

> **💡 Note:** Pages visibility follows project settings (Settings → General → Visibility → Pages). For a private project, only members may see it unless you change it.

### 20.9 The extra jobs you didn't define

In the pipeline you'll see extra steps such as **`test`** and **`deploy`** (or `pages:deploy`). You only defined `pages`; GitLab automatically adds the internal jobs needed to publish the site to Pages. That's why the `pages` job is "special".

---

## 21. Troubleshooting cheat sheet

| Symptom | Cause | Fix |
|---|---|---|
| `CI configuration is invalid` | YAML/keyword typo (`scripts`, bad indentation) | Use Pipeline editor validation; fix keyword/indent |
| `command not found` (e.g. `python`) | Default image (Ruby) lacks tool | Add `image: python` (or the right image) |
| `echos: command not found` | Typo in shell command | Fix command (used on purpose to test failures) |
| Later stages "Skipped" | Earlier stage failed | Fix failing job; or run manually |
| Artifact not created | Job failed / wrong path | Ensure success and correct `paths` |
| `No such file` after `cd` | File not in that dir | `cp` file into folder first |
| `Password is [MASKED]` | Masked variable | Expected behaviour |
| Can't mask variable | Value < 8 chars | Use ≥ 8 characters |
| `HTTP Basic: Access denied` | Password auth not allowed | Use Personal Access Token / SSH |
| `not allowed to force push ... protected branch` | Diverged history + protected `main` | Allow force push (temporarily) **or** `git pull --allow-unrelated-histories` |
| Pipeline slow / pending | Shared free runners | Be patient; use dedicated runner |
| Pipeline won't run (validation) | Account not verified | Verify email + phone; may need identity verification for shared runners |

---

## 22. Practice project ideas

1. Deploy a **Node.js** or **React** app with a pipeline (build → test → deploy).
2. Create an **AWS EC2** free-tier instance and deploy your static web page onto it from the pipeline (add SSH key as a *File*/masked variable).
3. Explore **collaboration**: branches, **merge requests**, protected branches, approvals.
4. Read the official docs (docs.gitlab.com → CI/CD YAML reference) to learn `rules`, `needs`, `cache`, `services`, `environments`, `include`, etc.

---

## 23. Quick reference / cheat sheet

### Minimal full pipeline template

```yaml
image: alpine:latest          # default image for all jobs

variables:                    # non-secret variables
  APP_ENV: "dev"

stages:
  - build
  - test
  - deploy

before_script:
  - echo "Starting job $CI_JOB_ID on branch $CI_COMMIT_BRANCH"

build:
  stage: build
  script:
    - mkdir -p output
    - echo "hello" > output/hello.txt
  artifacts:
    paths:
      - output
    expire_in: 30 days

test:
  stage: test
  script:
    - cat output/hello.txt
    - echo "Tests OK"

deploy:
  stage: deploy
  script:
    - echo "Deploying to $APP_ENV as $GITLAB_USER_NAME"
  when: manual                # requires a click
  allow_failure: false        # block pipeline until approved
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual
```

### Keywords learned

| Keyword | Purpose |
|---|---|
| `stages` | Order of stages |
| `stage` | Assign a job to a stage |
| `script` | Commands to run |
| `before_script` / `after_script` | Setup / cleanup around `script` (global or per job) |
| `image` | Docker image for the job |
| `artifacts: paths / expire_in / when / untracked` | Preserve job output |
| `when: manual` | Job runs only when triggered by a user |
| `only: main` / `rules:` | Restrict to branches/conditions |
| `pages` (job name) | Special job that publishes GitLab Pages from `public/` |

### Git commands used

```bash
git init
git status
git add *                       # or: git add <file>
git commit -m "message"
git remote add origin <https-url>
git branch -M main
git push -u origin main
git push -u origin main --force # only if needed & allowed
git pull origin main --allow-unrelated-histories
```

### Where things are in the GitLab UI

| Need | Path |
|---|---|
| Pipelines & history | **Build → Pipelines** |
| Run pipeline manually | Build → Pipelines → **Run pipeline** |
| Schedules | Build → **Pipeline schedules** |
| Edit YAML with validation | Build → **Pipeline editor** |
| Variables | Settings → **CI/CD → Variables** |
| Protected branches | Settings → **Repository → Protected branches** |
| Access tokens | Profile → Edit profile → **Access tokens** |
| Theme/preferences | Profile → **Preferences** |
| Website URL | **Deploy → Pages** |

---

*End of notes.*
