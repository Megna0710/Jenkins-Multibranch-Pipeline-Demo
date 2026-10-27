# Jenkins Multibranch Pipeline — Declarative CI/CD Demo

A beginner-friendly DevOps project demonstrating branch-aware CI/CD with Jenkins Declarative Pipeline, GitHub, automated checks, tests, artifact packaging, and a gated deploy-artifact stage.

## Pipeline stages

1. **Checkout** — checks out the SCM revision Jenkins selected and records the commit.
2. **Compile** — verifies Python syntax with `compileall`.
3. **Review** — runs a dependency-free AST syntax/quality gate.
4. **Test** — runs automated unit/integration-style HTTP endpoint tests.
5. **Package** — creates a versioned `.tar.gz`, checksum, and archives artifacts in Jenkins.
6. **Deploy** — only on `main` or `master`, prepares and archives a release bundle. This is a safe demo deployment artifact, not a production infrastructure deployment.


## Repository layout

```text
.
├── Jenkinsfile
├── app/
│   └── main.py
├── tests/
│   ├── test_app.py
│   └── test_review.py
├── scripts/review.py
├── .gitignore
├── .github/workflows/validate.yml
└── README.md
```

## Run locally (Windows PowerShell / Git Bash / Linux)

Requires Python 3.10+.

```bash
python --version
python -m compileall -q app tests scripts
python scripts/review.py
python -m unittest discover -s tests -p "test_*.py" -v
```

Run the sample HTTP service:

```bash
python -m app.main
```

Then open `http://localhost:8080/health`. Expected response:

```json
{"service":"jenkins-multibranch-demo","status":"healthy"}
```

Stop it with `Ctrl+C`.


## Configure Jenkins Multibranch Pipeline

1. Push this repository to GitHub.
2. Install a supported Jenkins LTS release and ensure the Jenkins agent has Git, Python 3, `tar`, and `sha256sum` available. The shell commands in this Jenkinsfile target a Linux agent.
3. Ensure Jenkins has the **Pipeline**, **Git**, and **Branch API** plugins (typically included/recommended with Jenkins setup).
4. In Jenkins, select **New Item** → enter a name → select **Multibranch Pipeline**.
5. Under **Branch Sources**, add **GitHub** or **Git**, then provide the repository URL. For a public repository, read access may not need credentials. For a private repository, use Jenkins Credentials; never put tokens in the Jenkinsfile.
6. Set **Script Path** to `Jenkinsfile` (repository root).
7. Save and select **Scan Multibranch Pipeline Now**. Jenkins should create a child job for each eligible branch containing a `Jenkinsfile`.
8. Push a commit to a branch and inspect that branch's build stages and archived artifacts.
9. Configure a GitHub webhook to your Jenkins endpoint only if Jenkins is reachable securely from GitHub. Otherwise use periodic scans or manual branch indexing.

## Demonstrate branch discovery

Create a feature branch, commit a small README change, and push it. Then create a hotfix branch similarly. Run **Scan Multibranch Pipeline Now**. Jenkins should discover the branches and create branch-specific jobs. The Deploy stage is intentionally skipped outside `main`/`master`.

```bash
git switch -c feature/update-readme
# edit README.md
git add README.md
git commit -m "docs: update README"
git push -u origin feature/update-readme
```

Repeat with `hotfix/example-fix` if desired.

## Important limitations

- The `Deploy` stage creates a release bundle and archives it; it does not publish to a production server or cloud platform. That keeps the starter assignment safe and runnable without credentials. A real deployment target can be added later.
- The Jenkinsfile uses POSIX shell commands, so use a Linux Jenkins agent (or adapt commands for Windows agents).
- Jenkins needs Python 3 installed on the selected agent. `agent any` means any eligible agent, not any operating system.
- A Multibranch Pipeline discovers branches; a webhook or scan schedule determines how quickly Jenkins notices changes.

