function addOutboundTracking() {
  const name = 'outbound-link-click';
  document.querySelectorAll('a').forEach((a) => {
    if (
      a.host !== window.location.host &&
      !a.getAttribute('data-umami-event')
    ) {
      a.setAttribute('data-umami-event', name);
      a.setAttribute('data-umami-event-url', a.href);
    }
  });
}

// Run on initial load
addOutboundTracking();

// Run again on SPA navigations
document.addEventListener('DOMContentLoaded', () => {
  // For Docusaurus route updates (React SPA), listen to pushes/replaceState
  const pushState = history.pushState;
  const replaceState = history.replaceState;

  function hook(func) {
    return function () {
      const result = func.apply(this, arguments);
      setTimeout(addOutboundTracking, 200); // re-run after DOM updates
      return result;
    };
  }

  history.pushState = hook(pushState);
  history.replaceState = hook(replaceState);

  window.addEventListener('popstate', () => {
    setTimeout(addOutboundTracking, 200);
  });
});
