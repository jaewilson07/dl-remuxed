# Class Validation System - Complete Setup

This document provides an overview of the complete class validation system for the domolibrary2 project.

## 📦 What's Included

The class validation system consists of several components designed to help systematically validate, refactor, and test all classes in the project:

### 1. Issue Template
**Location**: `.github/ISSUE_TEMPLATE/class-validation.md`

GitHub issue template that provides:
- Structured validation phases
- Detailed task checklists
- Acceptance criteria
- Environment variable documentation
- Implementation checklist

**Use**: Create individual issues manually via GitHub's issue creation interface

### 2. Comprehensive Guide
**Location**: `docs/class-validation-guide.md`

In-depth documentation covering:
- Detailed phase breakdowns with examples
- Entity hierarchy decision trees
- Code patterns (✅ good vs ❌ bad examples)
- Common issues and solutions
- Prioritization strategy

**Use**: Reference while working through class validation tasks

### 3. Quick Reference
**Location**: `docs/class-validation-quick-reference.md`

Condensed cheat sheet with:
- Quick start instructions
- Entity hierarchy diagrams
- Required components checklist
- Common patterns and anti-patterns
- Speed run guide for experienced contributors

**Use**: Quick lookup during implementation

### 4. Issue Generator Script
**Location**: `scripts/generate-class-validation-issues.py`

Python script that:
- Scans the classes directory
- Generates issue files for all classes
- Categorizes by priority
- Creates ready-to-import issue markdown files

**Use**: Bulk generate issues for all classes

### 5. Generated Issues Directory
**Location**: `EXPORTS/issues/`

Contains:
- Auto-generated issue files (one per class)
- README with import instructions
- Priority-based organization

**Use**: Bulk import issues or use as templates

## 🚀 Getting Started

### Step 1: Read the Documentation

Start by reading the guides in order:

```powershell
# Quick overview
code docs/class-validation-quick-reference.md

# Detailed guide (recommended)
code docs/class-validation-guide.md

# Issue template (to understand structure)
code .github/ISSUE_TEMPLATE/class-validation.md
```

### Step 2: Generate Issue Files

Generate issues for all classes:

```powershell
# Generate all issues
python scripts/generate-class-validation-issues.py

# Or just high priority classes
python scripts/generate-class-validation-issues.py --priority high
```

### Step 3: Import Issues to GitHub

Choose your import method:

#### Option A: Manual (Recommended for First-Time)
1. Navigate to GitHub Issues
2. Click "New Issue"
3. Select "Class Validation and Testing" template
4. Fill in the details for your target class

#### Option B: Bulk Import via GitHub CLI
```powershell
# Import all high priority issues
Get-ChildItem -Path "EXPORTS/issues/issue_*.md" | 
    Where-Object { $_.Name -match "(DomoUser|DomoDataset|DomoCard|DomoPage|DomoGroup)" } |
    ForEach-Object { gh issue create --body-file $_.FullName }
```

### Step 4: Work Through Issues

For each issue:
1. Read the full issue description
2. Work through phases 1-5 in order
3. Reference the guides as needed
4. Check off tasks as you complete them
5. Verify acceptance criteria before closing

## 📋 Recommended Workflow

### For Individual Contributors

1. **Pick an Issue**: Start with high-priority classes
2. **Phase 1**: Validate structure (30 min)
3. **Phase 2**: Analyze composition (30 min)
4. **Phase 3**: Verify route integration (30 min)
5. **Phase 4**: Validate manager (if applicable) (20 min)
6. **Phase 5**: Create/update tests (1-2 hours)
7. **Review**: Check acceptance criteria (15 min)
8. **Submit**: Create PR and link to issue

**Estimated time per class**: 2-4 hours depending on complexity

### For Teams

1. **Generate all issues**: Run the script once
2. **Import to GitHub**: Bulk import or create manually
3. **Assign issues**: Distribute across team members
4. **Track progress**: Use GitHub Projects or milestones
5. **Review PRs**: Ensure consistency across implementations
6. **Update documentation**: Keep guides current as patterns evolve

## 🎯 Priority Strategy

### Week 1: High Priority Classes (5 classes)
- DomoUser (reference implementation)
- DomoDataset
- DomoCard
- DomoPage
- DomoGroup

### Week 2: Medium Priority Classes (4+ classes)
- DomoRole
- DomoAccount
- DomoActivityLog
- DomoApplication

### Week 3+: Low Priority Classes
- Specialized features
- Legacy integrations
- Utility classes

## 📊 Tracking Progress

### Create a GitHub Project

```
Class Validation Project
├── Backlog (Not Started)
├── In Progress (1-5 tasks)
├── In Review (PR submitted)
└── Done (Merged & tested)
```

### Use Milestones

```
Milestone: High Priority Classes (Week 1)
Milestone: Medium Priority Classes (Week 2)
Milestone: Low Priority Classes (Ongoing)
```

### Label Strategy

Apply labels for filtering:
- `class-validation` - All validation issues
- `priority-high` - Start here
- `priority-medium` - Next batch
- `priority-low` - Lower priority
- `testing` - Testing-related work
- `refactor` - Code refactoring

## 🔧 Customization

### Modifying the Issue Template

Edit `.github/ISSUE_TEMPLATE/class-validation.md` to:
- Add/remove task items
- Adjust acceptance criteria
- Include project-specific requirements
- Update references

### Modifying the Generator Script

Edit `scripts/generate-class-validation-issues.py` to:
- Change priority classifications
- Adjust output format
- Add custom fields
- Modify priority logic

### Updating the Guides

Edit the documentation files to:
- Add new patterns discovered during validation
- Include additional examples
- Update with lessons learned
- Add troubleshooting tips

## 📚 File Reference

| File | Purpose | When to Use |
|------|---------|-------------|
| `.github/ISSUE_TEMPLATE/class-validation.md` | GitHub issue template | Creating individual issues manually |
| `docs/class-validation-guide.md` | Comprehensive guide | Learning the validation process |
| `docs/class-validation-quick-reference.md` | Quick lookup | During implementation |
| `scripts/generate-class-validation-issues.py` | Issue generator | Bulk creating issue files |
| `EXPORTS/issues/README.md` | Import instructions | Bulk importing to GitHub |
| `EXPORTS/issues/issue_*.md` | Generated issues | Individual class issues |

## 💡 Tips for Success

### For First-Time Contributors
1. **Start with DomoUser**: It's the reference implementation
2. **Read the full guide**: Don't skip the comprehensive guide
3. **One phase at a time**: Don't try to do everything at once
4. **Ask questions**: Create discussion issues for clarification
5. **Test frequently**: Run tests after each change

### For Experienced Contributors
1. **Use the quick reference**: Skip to what you need
2. **Follow patterns**: Copy from DomoUser, DomoDataset examples
3. **Batch similar tasks**: Do all structure validation first, then tests
4. **Document discoveries**: Update guides with new patterns found
5. **Speed run**: Experienced contributors can complete in 1-2 hours

### For Team Leads
1. **Set up tracking**: Create GitHub Project or use milestones
2. **Review PRs consistently**: Ensure pattern adherence
3. **Update documentation**: Keep guides current
4. **Pair new contributors**: Match experienced with newcomers
5. **Celebrate progress**: Recognize completed milestones

## 🔄 Maintenance

### Regular Updates

**Weekly**:
- Review closed issues for patterns
- Update guides with new examples
- Adjust priority classifications as needed

**Monthly**:
- Regenerate issues if template changes
- Update documentation with lessons learned
- Review and archive completed work

**Quarterly**:
- Evaluate overall progress
- Adjust strategy based on results
- Update tooling as needed

### Documentation Updates

When you discover:
- **New patterns**: Add to the comprehensive guide
- **Common issues**: Add to troubleshooting sections
- **Better approaches**: Update examples in quick reference
- **Tool improvements**: Update script or template

## 📞 Getting Help

### Resources
1. **Quick Reference**: Fast lookup for common patterns
2. **Comprehensive Guide**: Detailed explanations and examples
3. **DomoUser.py**: Reference implementation
4. **Test Examples**: tests/classes/DomoUser.py

### Support Channels
- **GitHub Discussions**: For general questions
- **GitHub Issues**: For bugs or template improvements
- **PR Comments**: For code-specific questions
- **Team Chat**: For real-time help (if applicable)

## ✅ Success Criteria

The class validation system is successful when:
- ✅ All classes follow entity hierarchy patterns
- ✅ All classes delegate to route functions
- ✅ All classes have working tests
- ✅ All classes have proper type hints
- ✅ All classes follow composition patterns
- ✅ Documentation is complete and accurate
- ✅ .env variables are documented
- ✅ Code passes all linting checks

## 🎉 Completion

Once all classes are validated:
1. Archive the EXPORTS/issues directory
2. Update README with completion status
3. Celebrate the achievement! 🎊
4. Move to maintenance mode

---

**System Version**: 1.0  
**Last Updated**: 2024  
**Maintained By**: domolibrary2 team
