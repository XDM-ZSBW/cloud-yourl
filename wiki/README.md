# 📚 Yourl.Cloud Wiki Documentation

**Last Updated**: 2025-08-14
**Project**: Yourl.Cloud Inc.
**Repository**: [https://github.com/XDM-ZSBW/cloud-yourl](https://github.com/XDM-ZSBW/cloud-yourl)

## 🎯 **Wiki Automation System** (Future Feature)

This wiki is planned to be automatically synchronized from the `wiki/` directory in the main repository using GitHub Actions in a future update. Currently, manual synchronization is required.

## 🔄 **How the Sync Will Work** (Future Implementation)

### **Planned Automated Workflow**
1. **Push Changes**: When you push changes to any file under `wiki/` to the main branch
2. **Trigger Workflow**: GitHub Actions will automatically detect the changes
3. **Sync Process**: The workflow will clone the wiki repository and sync all files
4. **Update Wiki**: Changes will be committed and pushed to the GitHub Wiki
5. **Verification**: The workflow will verify the sync was successful

**Note**: This automation is currently in development and not yet active.

### **Planned Sync Methods**
- **Primary**: `sync-wiki.yml` - Will use rsync and git commands (faster, no dependencies)
- **Alternative**: `sync-wiki-script.yml` - Will use the Python script (more features, dependency-aware)

**Status**: Both workflows are in development and not yet active.

## 📁 **Required Structure**

### **Essential Files**
- **`wiki/Home.md`** - Landing page (must exist)
- **`wiki/README.md`** - This file explaining the system
- **Other `.md` files** - Additional wiki pages

### **Directory Structure**
```
wiki/
├── Home.md                    # Landing page (required)
├── README.md                  # This file
├── KNOWLEDGE_HUB.md          # Knowledge hub
├── ARCHITECTURE_OVERVIEW.md  # System architecture
├── TECHNOLOGY_STACK.md       # Technology overview
├── EXTERNAL_RESOURCES.md     # External tools and resources
├── SECURITY.md               # Security policies
├── DEPLOYMENT_SUMMARY.md     # Deployment guide
└── [other documentation files]
```

## ✏️ **How to Add/Edit Pages**

### **Adding New Pages**
1. Create a new `.md` file in the `wiki/` directory
2. Use proper Markdown formatting
3. Add links to other wiki pages using `[[Page Name]]` or `[Page Name](PageName.md)`
4. Commit and push to main branch
5. **Manual step required**: Manually sync to GitHub Wiki until automation is implemented

### **Editing Existing Pages**
1. Modify any `.md` file in the `wiki/` directory
2. Save your changes
3. Commit and push to main branch
4. **Manual step required**: Manually sync to GitHub Wiki until automation is implemented

### **Deleting Pages**
1. Remove the `.md` file from the `wiki/` directory
2. Commit and push to main branch
3. **Manual step required**: Manually remove from GitHub Wiki until automation is implemented

## 🖼️ **Adding Images**

### **Image Storage Options**
- **Inside wiki/**: Store images in `wiki/images/` and reference them relatively
- **Outside wiki/**: Use raw URLs or GitHub raw content links

### **Recommended Approach**
```
wiki/
├── images/
│   ├── logo.png
│   ├── architecture.png
│   └── screenshots/
└── Home.md
```

**Reference in Markdown:**
```markdown
![Logo](images/logo.png)
![Architecture](images/architecture.png)
```

## 🔗 **Linking Between Pages**

### **Wiki Links (Recommended)**
```markdown
[[Page Name]]                    # Links to PageName.md
[[Page Name|Display Text]]       # Links with custom display text
```

### **Relative Links**
```markdown
[Page Name](PageName.md)         # Links to PageName.md
[Subdirectory Page](subdir/Page.md)  # Links to nested pages
```

### **External Links**
```markdown
[GitHub Repository](https://github.com/XDM-ZSBW/cloud-yourl)
[Yourl.Cloud Platform](https://yourl.cloud)
```

## 🧪 **Testing the Sync** (Future Feature)

### **Planned Test Process**
1. **Make a Change**: Edit any file under `wiki/`
2. **Commit & Push**: Push your changes to the main branch
3. **Check Actions**: Go to Actions tab to see the workflow running
4. **Verify Wiki**: Check the GitHub Wiki for your changes

**Current Status**: Manual testing and synchronization required.

### **Example Test**
```bash
# Edit a wiki file
echo "# Test Update" >> wiki/test.md

# Commit and push
git add wiki/test.md
git commit -m "test: add test wiki page"
git push origin main

# Check GitHub Actions and Wiki
```

## 📋 **Workflow Details** (Future Implementation)

### **Primary Workflow (sync-wiki.yml)** - In Development
- **Trigger**: Push to main with changes in `wiki/**`
- **Method**: rsync + git commands
- **Dependencies**: None (uses built-in tools)
- **Speed**: Fast execution (planned)
- **Status**: Development in progress

### **Alternative Workflow (sync-wiki-script.yml)** - In Development
- **Trigger**: Push to main with changes in `wiki/**` or `scripts/update_wiki.py`
- **Method**: Python script execution
- **Dependencies**: Python 3.11+, requirements.txt
- **Features**: Advanced processing, dependency management (planned)
- **Status**: Development in progress

## 🛠️ **Troubleshooting**

### **Current Limitations**
- **Automation Not Active**: Wiki automation workflows are not yet implemented
- **Manual Sync Required**: All wiki updates must be done manually until automation is complete
- **Development Status**: Workflows are in development and testing phase

### **Future Common Issues** (When Automation is Active)
- **Workflow Not Triggered**: Ensure you're pushing to main branch and files are under `wiki/`
- **Permission Errors**: Check that the workflow has `contents: write` permission
- **Sync Failures**: Verify the wiki repository exists and is accessible

### **Manual Sync** (Current Required Method)
Since automation is not yet implemented, manual sync is currently required:
```bash
# Clone the wiki repo
git clone https://github.com/XDM-ZSBW/cloud-yourl.wiki.git

# Copy files
cp -r wiki/* cloud-yourl.wiki/

# Commit and push
cd cloud-yourl.wiki
git add -A
git commit -m "Manual sync from wiki/ directory"
git push
```

## 📖 **Best Practices**

### **File Naming**
- Use descriptive names: `ARCHITECTURE_OVERVIEW.md` not `arch.md`
- Avoid spaces: Use underscores or hyphens
- Keep names short but clear

### **Content Organization**
- **Home.md**: Always the landing page with navigation
- **README.md**: System documentation and usage instructions
- **Feature-specific files**: Group related information together
- **Cross-references**: Link between related pages

### **Markdown Standards**
- Use proper headings (`#`, `##`, `###`)
- Include table of contents for long pages
- Use code blocks for examples
- Include links to external resources

## 🔍 **Monitoring & Logs**

### **GitHub Actions Logs**
- Check the Actions tab for workflow execution
- Review logs for any errors or warnings
- Verify sync completion and timing

### **Wiki Repository**
- Monitor the wiki repository for commits
- Check commit messages for sync history
- Verify file changes and additions

## 📈 **Performance & Optimization**

### **Sync Speed**
- **rsync workflow**: Typically completes in 1-2 minutes
- **Python script workflow**: May take 2-4 minutes depending on dependencies
- **Large files**: Consider image optimization for better performance

### **Efficiency Tips**
- Batch multiple wiki changes in single commits
- Use relative links to reduce external dependencies
- Optimize images before adding to wiki/

## 🚀 **Current Development & Future Enhancements**

### **Current Development Status**
- **Wiki Automation**: Core workflows in development
- **GitHub Actions Integration**: Basic structure implemented
- **Testing & Debugging**: Ongoing refinement of sync processes

### **Planned Features** (Post-Implementation)
- **Selective Sync**: Sync only changed files for faster updates
- **Conflict Resolution**: Handle merge conflicts automatically
- **Backup System**: Automatic wiki backups before sync
- **Notification System**: Slack/Discord notifications on sync completion

### **Integration Options**
- **Slack Integration**: Notify team of wiki updates
- **Discord Webhooks**: Real-time sync status updates
- **Email Notifications**: Summary reports of wiki changes

---

## 🔗 **Quick Links**

- **[🏠 Home](Home.md)** - Main wiki landing page
- **[🧠 Knowledge Hub](KNOWLEDGE_HUB.md)** - Central documentation
- **[🔧 Technology Stack](TECHNOLOGY_STACK.md)** - Technology overview
- **[🔗 External Resources](EXTERNAL_RESOURCES.md)** - Tools and integrations
- **[🏗️ Architecture](ARCHITECTURE_OVERVIEW.md)** - System design
- **[🔐 Security](SECURITY.md)** - Security policies

---

**Yourl.Cloud Inc.** - Building the future of trust-based AI systems for families worldwide.

*Last updated: 2025-08-14*
