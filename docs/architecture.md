# Architecture and execution flow

```text
Developer
   | git push
   v
GitHub repository (main / feature/* / hotfix/*)
   | webhook or Multibranch scan
   v
Jenkins Multibranch Pipeline
   | discovers branches containing Jenkinsfile
   +--> branch job: Checkout
          -> Compile
          -> Review
          -> Test
          -> Package -> archived build artifact
          -> Deploy artifact (main/master only)
```

Each branch runs its own pipeline definition from that branch's `Jenkinsfile`. Sequential stages stop on an unhandled command failure, so failed validation does not progress to packaging or deployment.
