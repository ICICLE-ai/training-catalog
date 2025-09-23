import React from 'react';
import TOC from '@theme-original/TOC';


const collator = new Intl.Collator('en', { numeric: true, sensitivity: 'base' });

function keyOf(value) {
  return value.replace(/^[^A-Za-z0-9]+/, '').trim();
}

function deepSortTOC(items = []) {
  const withSortedChildren = items.map((item) => ({
    ...item,
    children: item.children ? deepSortTOC(item.children) : undefined,
  }));

  return withSortedChildren.sort((a, b) =>
    collator.compare(keyOf(a.value), keyOf(b.value))
  );
}

export default function TOCWrapper(props) {
  const sortedTOC = deepSortTOC(props.toc || []);
  return <TOC {...props} toc={sortedTOC} />;
}
