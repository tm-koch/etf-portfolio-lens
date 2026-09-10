## ADDED Requirements

### Requirement: Configure workflow publication identity
The scheduled GitHub Pages publishing workflow SHALL configure its checkout with the GitHub Actions bot identity before invoking the publisher. The identity configuration SHALL use the non-personal `github-actions[bot]` name and GitHub Actions noreply email, while the publisher SHALL remain usable for manual invocations without imposing that identity.

#### Scenario: Publisher commits with automation identity

- **WHEN** the Actions checkout is complete and the workflow is about to invoke the Pages publisher
- **THEN** the workflow configures `user.name` as `github-actions[bot]` and `user.email` as `41898282+github-actions[bot]@users.noreply.github.com`

#### Scenario: Publisher does not require runner-global identity

- **WHEN** the publisher runs manually with its own caller-provided Git identity
- **THEN** the publisher does not overwrite that identity or require workflow-only configuration commands
