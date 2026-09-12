# DoveWAI AXI / Resource / Protect Integration Map v0.1

Status: implementation map created; testing intentionally deferred until all implementation phases are complete.

## Objective

Adapt the strongest patterns from gh-axi, quota-axi, Automic Vault, ego-lite, worktrunk, codegraph-style systems, semantic review tools, Chandra-style document intelligence, Transloco, Angular testing tooling, device/capability detection, Web API wrappers, and efficient fine-tuning systems into DoveWAI-owned, vendor-neutral components.

This is not a dependency-collection plan. DoveWAI owns the contracts and orchestration; external projects are references, optional adapters, or benchmarks.

## Non-negotiable rules

1. Local-first and cross-platform.
2. No permanent dependency on restrictive or commercial-only model/runtime assets.
3. Least authority for agents and tools.
4. Compact agent-facing interfaces; full evidence retained separately.
5. Provider-neutral contracts.
6. Every mutation produces provenance and receipt data.
7. External source/license provenance is recorded before adaptation.
8. No automated test gate runs until Phase 8, after implementation phases complete.
9. GitHub cloud automation must remain manual unless explicitly changed later.

## Target architecture

```text
DoveWAI Personal / Software Factory
              |
          Worker Runtime
   +----------+----------+
   |          |          |
 Worktree   Browser    Task Context
   |          |          |
   +----------+----------+
              |
             AXI
    compact agent tool adapters
              |
       Resource Broker
 quota/cost/compute/storage/health
              |
           Protect
 capability policy + secret custody
              |
   Harness / Semantic Verification
              |
       Ark + Code Intelligence
              |
       Radar -> Miner -> Ark
              |
 Translation / Document / Training
```

## Phase 0 — Contracts and provenance

Define shared protocol-compatible extension contracts without changing the v0.2 core lifecycle:

- AXI invocation envelope
- resource-state evidence
- authorization decision evidence
- worker isolation metadata
- code-intelligence evidence
- semantic-review evidence
- external-source provenance and license decision

Map all of them to existing v0.2 Artifact, ExecutionEvent, Verification, Provenance, Capability and WorkReceipt objects rather than inventing a second lifecycle.

Deliverables:

- `axi.invocation.v0.1`
- `resource.snapshot.v0.1`
- `protect.authorization.v0.1`
- `worker.workspace.v0.1`
- `codegraph.snapshot.v0.1`
- `semantic.review.v0.1`
- `source.license-decision.v0.1`

## Phase 1 — DoveWAI AXI

Adapt concepts from gh-axi and similar agent-oriented interfaces.

Build owned adapters for:

- Git/GitHub
- shell/process
- filesystem
- browser
- HTTP/API
- models
- resource broker
- secrets/capabilities

Rules:

- no TUI for autonomous paths
- deterministic exit codes
- bounded output by default
- explicit full-output escape hatch
- structured error category + recovery hint
- destructive actions require explicit intent
- stdin/file-descriptor secret delivery where supported
- raw evidence stored outside the compact agent context

Do not make DoveWAI GitHub-only. GitHub is the first provider; GitLab/Gitea/Forgejo/Azure DevOps remain future adapters.

## Phase 2 — Resource Broker

Adapt quota-axi's strongest patterns but expand them beyond model quotas.

Normalized domains:

- provider/model quota windows
- projected exhaustion/runway
- confidence/staleness
- API rate limits
- cloud credits/budget
- CPU/GPU/NPU availability
- RAM/VRAM
- local/NAS storage
- endpoint health
- latency
- privacy/data-locality restrictions
- task capability fit

The Resource Broker reports evidence. Planner performs routing.

Provider adapters must not silently refresh or mutate credentials except through explicit provider-supported delegated mechanisms recorded as events.

## Phase 3 — Protect authorization and secret custody

Adapt Automic Vault concepts without copying its macOS-only runtime architecture.

Cross-platform backends:

- Windows: DPAPI/Credential Manager or stronger supported native backend
- Linux: Secret Service/keyring or encrypted fallback
- macOS: Keychain

Policy inputs:

- verified worker/launcher identity
- task ID
- requested capability
- tool
- target
- arguments
- working directory
- credential names, never plaintext values in policy logs
- requested duration

Decisions:

- ALLOW
- REQUIRE_APPROVAL
- DENY

Temporary grants are task-scoped, capability-scoped, target-scoped and expiring.

Direct secret disclosure is a separate capability and denied by default.

## Phase 4 — Worker isolation

Adapt Worktrunk and ego-lite architectural ideas.

Each autonomous worker gets:

- task ID
- isolated Git worktree/branch
- isolated browser/session space where possible
- scoped tool capabilities
- scoped credentials
- resource budget
- separate logs/evidence
- receipt namespace

Worker cleanup must be idempotent and must not delete unmerged or unreferenced work without an explicit policy decision.

Browser control must use an owned provider-neutral contract. Playwright/CDP/native browser bridges may be adapters. A proprietary browser binary must never be required for protocol compliance.

## Phase 5 — Code intelligence and semantic review

Build DoveWAI-owned persistent repository intelligence from permissively licensed parser/indexing components.

Core graph:

- files/modules
- symbols
- imports
- calls
- inheritance/implementation
- API contracts
- configuration references
- tests
- dependency edges
- git/change relationships
- optional data-flow/security edges

Required properties:

- incremental updates
- filesystem/source-of-truth reconciliation
- compact local store
- cross-platform
- multiple-language parser adapters
- query API optimized for agents

Semantic review evaluates a change against graph impact, intended behaviour, security constraints and historical contracts. LLM review is advisory evidence, never the sole gate.

## Phase 6 — Knowledge, translation and document ingestion

### Document Intelligence

Adapt Chandra-style separation of input, inference and structured output, but keep OCR/model providers replaceable.

Outputs should preserve:

- source hash
- page/region coordinates
- reading order
- tables/math/images
- source language
- extracted structured text
- translation links
- confidence/provenance

Restricted model weights are benchmark/reference only unless separate commercial terms are accepted.

### Translation

Adapt Transloco and other i18n concepts into DoveWAI-Translation:

- UI localization
- document/chat/search translation
- locale/currency/date/number formatting
- fallback chains
- source-language preservation
- translation cache
- confidence/provenance

English normalization for search must never discard the original text.

## Phase 7 — Training and capability adaptation

Use LlamaFactory/PEFT/Transformers-class systems as replaceable training adapters, not as DoveWAI's identity.

Support:

- LoRA/QLoRA
- quantized training paths
- dataset contracts
- checkpoint manifests
- hardware-aware planning
- resumable jobs
- model-license provenance

No training data derived from restricted-model outputs may enter DoveWAI training sets unless the relevant license permits it and a license decision record exists.

## Phase 8 — Final verification gate (DEFERRED UNTIL ALL ABOVE COMPLETE)

Only after Phases 0–7 are implemented:

1. schema/contract validation
2. unit tests
3. integration tests
4. behaviour tests
5. browser/API tests
6. security tests
7. semantic-regression tests
8. cross-platform tests
9. offline-mode tests
10. failure/recovery tests
11. resource-routing tests
12. authorization bypass tests
13. provenance/license-policy tests
14. WorkReceipt verification

Testing remains deliberately postponed until implementation completion, per current project directive.

## Repository ownership map

- DoveWAI-Protocol: contracts, profiles, portable evidence semantics
- DoveWAI-Personal: user-facing agent/runtime consumption
- DoveWAI-Engineering-Harness: AXI execution adapters, workers, verification orchestration
- DoveWAI-Protect: authorization, credential custody, security policy
- DoveWAI-Research-Radar: discovery, trending/research acquisition, source metadata
- DoveWAI-Miner: extraction, normalization, license/provenance classification
- DoveWAI-Ark: evidence, knowledge, graph and compact retained state
- DoveWAI-Translation: translation/localization services
- DoveWAI-Training / Compute: training adapters and hardware-aware execution

Where a named repo does not yet exist or is not exposed, implement the capability in the closest existing owner module and split later only when justified.

## External reference disposition

| Reference | Disposition |
|---|---|
| gh-axi | adapt architecture/code where license permits; DoveWAI owns provider-neutral AXI |
| quota-axi | adapt normalized provider/runway patterns; extend to compute/cost/storage |
| Automic Vault | adapt security concepts; build cross-platform DoveWAI implementation |
| ego-lite | adapt workspace/browser-isolation concepts; no binary dependency |
| worktrunk | adapt safe worktree lifecycle and parallel-worker patterns |
| codegraph family | compare parsers/indexers; build DoveWAI-owned graph contract/store |
| Recurse ML / reslop | benchmark semantic review; build owned review pipeline |
| Chandra | architecture/benchmark; restricted model assets are not baseline dependency |
| Transloco | adapt localization/fallback/cache concepts into broader Translation service |
| Angular Testing Library | adapt behaviour-first verification philosophy |
| jest-preset-angular | adapt test-preset concept into framework-neutral Harness presets |
| ngx-device-detector | adapt into capability detection rather than UA-only identity |
| ng-web-apis | adapt Web capability-provider abstraction |
| LlamaFactory | training adapter/reference, not permanent control plane |

## Completion definition before tests

Implementation phase is considered complete only when every Phase 0–7 contract/module has:

- owned interface
- provider boundary
- fail-closed error semantics where security-sensitive
- provenance/license metadata path
- documented integration owner
- no unresolved circular dependency
- no mandatory proprietary component
- offline/local fallback where technically possible

Then Phase 8 begins.