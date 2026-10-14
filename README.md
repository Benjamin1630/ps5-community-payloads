# ps5-community-payloads

A custom source for itsPLK's [Payload Manager](https://github.com/itsPLK/ps5-payload-manager) with:

- [Tailscale](https://github.com/holdmysocks/ps5-tailscale) (holdmysocks)
- [Prospero Manager](https://github.com/notmaj0r/ProsperoMgr) (notmaj0r)

Add this URL under Settings → Manage Sources → Add Source:

```
https://raw.githubusercontent.com/Benjamin1630/ps5-community-payloads/main/payloads.json
```

`payloads.json` is rebuilt daily from each project's latest GitHub release by `build.py`. Files are downloaded straight from the upstream releases and checked against GitHub's SHA-256 digests. Nothing is rehosted here.
