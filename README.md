# CreatorDeals

Independent buying guides for video, audio, and AI creator software. Twenty English merchant profiles are sourced to official product pages; German and Japanese launch pages cover the home page and three selected merchants. No coupon codes or affiliate links are active at launch.

Run `npm ci && npm run build`. Run `python -m pip install jsonschema==4.25.1 && python scripts/refresh_deals.py` to validate and archive expired offers. Daily Actions runs the same script; `data/raw/` is the file provider input for future manually verified public offers. Each offer needs an official source URL and dated verification.

Growth expectations: allow 3–6 months for crawling and discovery. At 90 days, assess indexing and impressions, not revenue. Google Search Console verification is a manual post-deploy step. A custom domain can be set later with `SITE_URL`; default is the Pages domain.
