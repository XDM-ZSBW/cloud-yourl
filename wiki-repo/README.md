# 📚 Yourl.Cloud Wiki Documentation

**Last Updated**: 2025-08-14
**Project**: Yourl.Cloud Inc.
**Repository**: [https://github.com/XDM-ZSBW/cloud-yourl](https://github.com/XDM-ZSBW/cloud-yourl)

## 🎯 **Wiki Automation System**

This wiki is automatically synchronized from the `wiki/` directory in the main repository. Any changes you make to files in the `wiki/` folder will automatically update the GitHub Wiki after you push to the main branch.

## 🔄 **How the Sync Works**

### **Automated Workflow**
1. **Push Changes**: When you push changes to any file under `wiki/` to the main branch
2. **Trigger Workflow**: GitHub Actions automatically detects the changes
3. **Sync Process**: The workflow clones the wiki repository and syncs all files
4. **Update Wiki**: Changes are committed and pushed to the GitHub Wiki
5. **Verification**: The workflow verifies the sync was successful

### **Two Sync Methods**
- **Primary**: `sync-wiki.yml` - Uses rsync and git commands (faster, no dependencies)
- **Alternative**: `sync-wiki-script.yml` - Uses the Python script (more features, dependency-aware)

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
5. The wiki will automatically update

### **Editing Existing Pages**
1. Modify any `.md` file in the `wiki/` directory
2. Save your changes
3. Commit and push to main branch
4. The wiki will automatically update

### **Deleting Pages**
1. Remove the `.md` file from the `wiki/` directory
2. Commit and push to main branch
3. The page will be automatically removed from the wiki

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

## 🧪 **Testing the Sync**

### **Test Process**
1. **Make a Change**: Edit any file under `wiki/`
2. **Commit & Push**: Push your changes to the main branch
3. **Check Actions**: Go to Actions tab to see the workflow running
4. **Verify Wiki**: Check the GitHub Wiki for your changes

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

## 📋 **Workflow Details**

### **Primary Workflow (sync-wiki.yml)**
- **Trigger**: Push to main with changes in `wiki/**`
- **Method**: rsync + git commands
- **Dependencies**: None (uses built-in tools)
- **Speed**: Fast execution

### **Alternative Workflow (sync-wiki-script.yml)**
- **Trigger**: Push to main with changes in `wiki/**` or `scripts/update_wiki.py`
- **Method**: Python script execution
- **Dependencies**: Python 3.11+, requirements.txt
- **Features**: Advanced processing, dependency management

## 🛠️ **Troubleshooting**

### **Common Issues**
- **Workflow Not Triggered**: Ensure you're pushing to main branch and files are under `wiki/`
- **Permission Errors**: Check that the workflow has `contents: write` permission
- **Sync Failures**: Verify the wiki repository exists and is accessible

### **Manual Sync**
If automation fails, you can manually sync:
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

## 🚀 **Future Enhancements**

### **Planned Features**
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
