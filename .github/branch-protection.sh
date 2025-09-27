# Code Live - Branch Protection Configuration
# GitHub CLI commands to set up branch protection for main

# Set up branch protection for main branch
gh api repos/TUNEZILLA-zz/polygot-code-sampler/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["ci: test","ci: lint","ci: pre-commit","ci: golden-stability","ci: matrix-smoke","ci: publish-dashboard (dry-run)"]}'
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true,"require_code_owner_reviews":true}'
  --field restrictions='{"users":[],"teams":[],"apps":[]}' \
  --field allow_force_pushes=false \
  --field allow_deletions=false \
  --field block_creations=false \
  --field required_conversation_resolution=true

# Set up repository rulesets (if available)
gh api repos/TUNEZILLA-zz/polygot-code-sampler/rulesets \
  --method POST \
  --field name="Code Live Protection Rules" \
  --field target="branch" \
  --field enforcement="active" \
  --field conditions='{"ref_name":{"include":["refs/heads/main","refs/heads/develop"]}}' \
  --field rules='[{"type":"max_file_size","parameters":{"max_file_size":104857600}},{"type":"required_signatures","parameters":{}},{"type":"required_linear_history","parameters":{}}]'

echo "✅ Branch protection configured for main and develop branches"
echo "🔒 Required checks: ci: test, ci: lint, ci: pre-commit, ci: golden-stability, ci: matrix-smoke, ci: publish-dashboard (dry-run)"
echo "👥 Required: 1 approving review, code owner reviews, dismiss stale reviews"
echo "🚫 Blocked: Force pushes, deletions, files > 100MB, unsigned commits"
echo "📏 Required: Linear history, conversation resolution"
