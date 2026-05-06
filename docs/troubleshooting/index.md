# Troubleshooting

Common issues and solutions for DClaw Recruit.

## Quick Diagnostics

```bash
# Check app pods
kubectl get pods -n dclaw-recruit

# Check logs
kubectl logs -n dclaw-recruit deployment/dclaw-recruit-backend

# Check database
kubectl get clusters -n dclaw-recruit
```

## Sections

- [Common Issues](./common-issues)
- [FAQ](./faq)
