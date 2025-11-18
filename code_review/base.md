> Last updated: 2025-11-17

# Base Layer Code Review (DomoLibrary2)

This document captures a focused review of the base layer in `src/domolibrary2/base/`
(`base.py`, `entities.py`, `entities_federated.py`, `exceptions.py`, `relationships.py`).
The goal is to minimize AI slop, remove anti-patterns, and tighten consistency
before reviewing auth, routes, and classes.

## Findings

| Severity | File/Location | Details |
| --- | --- | --- |
| critical | `src/domolibrary2/base/base.py: DomoBase.to_dict` | `except (Exception)` in the property-serialization loop violates the rule that library code must never catch bare `Exception`. It can mask genuine programming bugs and contradicts `error-design.instructions.md`. **Fix**: Narrow the catch to specific expected exceptions (e.g. `AttributeError`, `KeyError`, `TypeError`), or remove the blanket catch and let unexpected exceptions surface so tests can catch them. |
| major | `src/domolibrary2/base/entities.py: DomoEntity.refresh` | `refresh()` calls `type(self).get_entity_by_id(auth=self.auth, entity_id=self.id, debug_num_stacks_to_drop=..., debug_api=..., session=..., **kwargs)` while the abstract method signature is `async def get_entity_by_id(cls, auth: DomoAuth, entity_id: str)`. This implicit, undocumented contract invites divergence. **Fix**: Update the abstract signature to include the full parameter set (with defaults) and document it clearly, or introduce a dedicated non-abstract helper with a well-defined contract that `refresh` calls. |
| major | `src/domolibrary2/base/entities.py: DomoEntity._name` | `_name` raises `NotImplementedError` if `name` is missing, but `_name` is not abstract and nothing in base guarantees `name` exists. This is a brittle pattern and easy to forget in subclasses. **Fix**: Either make `_name` an abstract property and require direct implementation, or establish a standard `name` attribute requirement and document it clearly (or remove `_name` if not used consistently). |
| major | `src/domolibrary2/base/relationships.py: DomoRelationship.__eq__` | `__eq__` assumes `other` has `parent_entity` and `entity` attributes without type checking, so comparing to any other type can raise `AttributeError`. **Fix**: Guard with `if not isinstance(other, DomoRelationship): return NotImplemented` (or `False`) before accessing attributes. |
| major | `src/domolibrary2/base/relationships.py: DomoRelationship` docstring | The docstring describes fields (`relative_id`, `relative_class`, `relative_entity`) that no longer exist; actual fields are `relationship_type`, `parent_entity`, `entity`, `metadata`. This is documentation drift likely from earlier refactors. **Fix**: Rewrite the docstring to match the current fields and semantics (parent/child entity, `ShareAccount` role, `metadata`). |
| major | `src/domolibrary2/base/entities_federated.py: DomoFederatedEntity / DomoPublishedEntity` | Several abstract methods (`get_subscription`, `get_parent_publication`, `get_parent_content_details`, `get_federated_parent`) contain commented-out pseudo-implementations and then just `raise NotImplementedError`. This looks like incomplete scaffolding that will drift. **Fix**: Remove the commented pseudo-logic and tighten docstrings to minimal, clear contracts, or extract any reusable pieces into shared helpers that are actually used. |
| minor | `src/domolibrary2/base/exceptions.py: DomoError.__init__` | `DomoError` mixes `message` and `exception` into the base `Exception` message but does not override `__str__`. `self.message` may not match `str(e)`, and `message` may be non-string. **Fix**: Optionally implement `__str__`/`__repr__` to use `_generate_default_message` consistently, and consider normalizing `self.message` to a string. |
| minor | `src/domolibrary2/base/base.py: DomoEnumMixin.get/_missing_` | `get` and `_missing_` both iterate over `cls` with `# type: ignore` and no precise type hints. Functionally fine, but loose typing and duplication increase maintenance friction. **Fix**: Add type hints to `get` (e.g. `value: Any -> Any` or a more precise union) and re-evaluate whether both `get` and `_missing_` are needed. |
| minor | `src/domolibrary2/base/entities.py: DomoManager.get` | The abstract `get` method uses `*args, **kwargs` with no return type and a very generic docstring. This makes manager patterns harder to reason about and type check. **Fix**: Introduce a pattern (e.g. return type `list[DomoEntity]` or an async iterator) and document it; at minimum, add a return type annotation. |
| minor | `src/domolibrary2/base/entities.py: DomoSubEntity.from_parent` | `from_parent` blindly returns `cls(parent=parent)` with no validation; subclasses that require extra fields can easily misuse it. **Fix**: Document that base `from_parent` is only appropriate for simple subentities, and encourage subclasses to override it with a more complete signature when needed. |
| nit | `src/domolibrary2/base/base.py`, `src/domolibrary2/base/relationships.py` | Some docstrings are verbose and marketing-style ("unified relationship system", "relationship-centric"). Not harmful, but can obscure the essential contract for human readers and AI. **Fix**: Gradually trim docstrings to emphasize behavior and contracts rather than high-level slogans. |
| nit | `src/domolibrary2/base/relationships.py: ShareAccount` | Docstring says "Types of relationships between Domo entities" but enum name is `ShareAccount`; some members (`MEMBER`, `PARENT`, `CHILD`) extend beyond strict "sharing" semantics. **Fix**: Either tighten the docstring to match "sharing roles", or consider renaming/refactoring if used more broadly. |

## Implementation Plan

This plan focuses on the base layer; later passes will extend the same discipline
to auth, routes, and classes.

### 1. Tighten `DomoBase.to_dict` exception handling (critical)

**Goal**: Remove the bare `Exception` catch and align with `error-design.instructions.md`.

**Steps**:
1. In `src/domolibrary2/base/base.py`, inside `DomoBase.to_dict`, replace:

   ```python
   except (Exception):  # pragma: no cover - defensive; skip failing properties
       continue
   ```

   with a narrowed set of exceptions, for example:

   ```python
   except (AttributeError, KeyError, TypeError):  # pragma: no cover
       continue
   ```

2. Run targeted tests that exercise entity `to_dict` behavior indirectly via classes
   (e.g. `DomoDataset`, `DomoUser`) to ensure no unexpected breakage.

   ```pwsh
   pytest tests/classes -k "DomoDataset or DomoUser" -v
   ```

### 2. Align `DomoEntity.refresh` with `get_entity_by_id` (major)

**Goal**: Make the abstract contract explicit so subclasses implement the
same signature that `refresh` relies on.

**Steps**:
1. In `src/domolibrary2/base/entities.py`, update the abstract method signature:

   ```python
   @classmethod
   @abc.abstractmethod
   async def get_entity_by_id(
       cls,
       auth: DomoAuth,
       entity_id: str,
       debug_num_stacks_to_drop: int = 2,
       debug_api: bool = False,
       session: httpx.AsyncClient | None = None,
       **kwargs,
   ):
       ...
   ```

2. Update the docstring to document these parameters and their intended
   behavior.
3. Scan subclasses implementing `get_entity_by_id` to ensure their signatures
   and usages are compatible with the new base contract.
4. Run tests that exercise `refresh()` on representative entities, if present.

### 3. Clarify `DomoEntity._name` semantics (major)

**Goal**: Avoid brittle reliance on an implicit `name` attribute.

**Steps**:
1. Decide on the preferred pattern:
   - **Option A**: Make `_name` an abstract property and require subclasses to
     implement it.
   - **Option B**: Remove `_name` from base and rely on concrete classes to
     expose a `name` attribute or property as needed.
2. Implement the chosen option in `src/domolibrary2/base/entities.py`.
3. Update any call sites that depend on `_name` (via search for `._name`).

### 4. Fix `DomoRelationship.__eq__` and docstring drift (major)

**Goal**: Make equality safe and documentation accurate.

**Steps**:
1. In `src/domolibrary2/base/relationships.py`, change `__eq__` to:

   ```python
   def __eq__(self, other: object) -> bool:
       if not isinstance(other, DomoRelationship):
           return NotImplemented
       return (
           self.parent_entity.id == other.parent_entity.id
           and self.relationship_type == other.relationship_type
           and self.entity.id == other.entity.id
       )
   ```

2. Rewrite the `DomoRelationship` docstring to describe the actual fields:
   - `relationship_type: ShareAccount`
   - `parent_entity`
   - `entity`
   - `metadata`
3. Verify that equality is exercised by tests or add a small unit test that
   compares relationships and checks deduplication behavior.

### 5. Clean up federated/published entity scaffolding (major)

**Goal**: Reduce AI-style pseudo-code and clarify contracts.

**Steps**:
1. In `src/domolibrary2/base/entities_federated.py`, remove commented-out
   pseudo-implementation blocks from:
   - `get_subscription`
   - `get_parent_publication`
   - `get_parent_content_details`
   - `get_federated_parent`
2. Tighten docstrings for these abstract methods to a concise description of
   inputs/outputs and behavior (no implied internal details).
3. If there are concrete implementations relying on this pseudo-logic, extract
   the shared behavior into small helper functions and call those from the
   concrete classes instead of leaving it commented in the base.

### 6. Refine `DomoError` and enum helpers (minor)

**Goal**: Improve consistency and type clarity without changing behavior.

**Steps**:
1. In `src/domolibrary2/base/exceptions.py`, add a `__str__` implementation to
   `DomoError` that returns `self._generate_default_message`. Ensure that this
   does not conflict with logging expectations.
2. Consider normalizing `message` to a string when stored on the instance, or
   clearly documenting that it may come from non-string API responses.
3. In `src/domolibrary2/base/base.py`, add type hints for `DomoEnumMixin.get`
   and review whether both `get` and `_missing_` are needed; if not, simplify.

### 7. Improve manager and sub-entity contracts (minor)

**Goal**: Make base contracts clearer for consumers and type checkers.

**Steps**:
1. In `DomoManager.get`, add a return type annotation (e.g. `-> Any` or a more
   specific collection type) and refine the docstring to describe expected
   behavior.
2. Document `DomoSubEntity.from_parent` as a convenience for simple cases and
   encourage subclasses with extra required fields to override it.

### 8. Trim overly verbose docstrings (nit)

**Goal**: Reduce noise and AI-style marketing language.

**Steps**:
1. Pass through `base.py` and `relationships.py` and selectively trim
   descriptions that do not add concrete behavioral information.
2. Keep examples and contracts; remove slogans.

### 9. Validation and regression checks

After changes are implemented:

1. Run linters and formatters:

   ```pwsh
   .\scripts\format-code.ps1
   .\scripts\lint.ps1
   ```

2. Run targeted tests for base-dependent classes (datasets, users, etc.):

   ```pwsh
   pytest tests/classes -k "DomoDataset or DomoUser" -v
   ```

3. If available, run any existing relationship/federation tests to ensure
   `DomoRelationship` and federated entities behave as expected.

---

Subsequent review passes will apply a similar approach to auth structures,
routes, and classes, using this base layer as the foundation for consistent
patterns and stricter error-handling across domolibrary2.
