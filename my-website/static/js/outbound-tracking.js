import {useEffect} from 'react';
import {useLocation} from '@docusaurus/router';

function trackPageview(url) {
  if (window.umami?.trackView) {
    window.umami.trackView(url, document.referrer);
  } else if (window.umami?.track) {
    window.umami.track('pageview', { url });
  }
}

function isExternalLink(a) {
  const href = a.getAttribute('href');
  if (!href) return false;
  // Skip non-http(s) schemes
  if (/^(mailto:|tel:|javascript:)/i.test(href)) return false;
  const u = new URL(href, window.location.origin);
  return u.origin !== window.location.origin;
}

export default function UmamiRouteAndOutbound() {
  const {pathname, search, hash} = useLocation();

  // Track every SPA URL change
  useEffect(() => {
    const url = `${pathname}${search || ''}${hash || ''}`;
    trackPageview(url);
  }, [pathname, search, hash]);

  // Track outbound link clicks via event delegation
  useEffect(() => {
    const onClick = (e) => {
      const a = e.target.closest?.('a');
      if (!a || !isExternalLink(a)) return;

      // Optional: strip query/hash to reduce cardinality
      const u = new URL(a.href);
      const href = u.href; // or `${u.origin}${u.pathname}`

      // Fire-and-forget; don't block navigation
      window.umami?.track?.('outbound_link', { href });
    };

    document.addEventListener('click', onClick, { capture: true });
    return () => document.removeEventListener('click', onClick, { capture: true });
  }, []);

  return null;
}
