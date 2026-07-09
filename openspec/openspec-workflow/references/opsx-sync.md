# /opsx:sync — 同步 delta specs 到主规格

## 用途
将变更中的 delta specs 智能合并到主规格文件（`openspec/specs/<capability>/spec.md`）。

## 输入
可选：指定变更名。

## 步骤

1. **选择变更**
   ```
   openspec list --json
   ```
   只展示有 delta specs 的变更

2. **查找 delta specs**
   `openspec/changes/<name>/specs/*/spec.md`

3. **智能合并**
   对每个 delta spec：

   **ADDED Requirements** → 如果主规格中没有则添加，已存在则更新
   **MODIFIED Requirements** → 找到对应 requirement，只应用变更（添加/修改 scenario）
   **REMOVED Requirements** → 从主规格中移除整个 requirement 块
   **RENAMED Requirements** → FROM → TO

4. **展示摘要**

## Delta Spec 格式参考
```markdown
## ADDED Requirements

### Requirement: New Feature
The system SHALL do something new.

#### Scenario: Basic case
- **WHEN** user does X
- **THEN** system does Y

## MODIFIED Requirements

### Requirement: Existing Feature
#### Scenario: New scenario to add
- **WHEN** user does A
- **THEN** system does B

## REMOVED Requirements

### Requirement: Deprecated Feature

## RENAMED Requirements

- FROM: `### Requirement: Old Name`
- TO: `### Requirement: New Name`
```
