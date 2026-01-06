import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import ExecutionEnvironment from '@docusaurus/ExecutionEnvironment';
import {useEffect, useState} from 'react';

import Heading from '@theme/Heading';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  const { heroHeading, heroDescription } = siteConfig.customFields;
  const [sanitizedDescription, setSanitizedDescription] = useState(heroDescription);
  
  // Sanitize HTML on client-side only to prevent SSR Buffer polyfill issues
  useEffect(() => {
    if (ExecutionEnvironment.canUseDOM) {
      import('isomorphic-dompurify').then((DOMPurify) => {
        const sanitized = DOMPurify.default.sanitize(heroDescription, {
          ALLOWED_TAGS: ['p', 'br', 'b', 'strong', 'iframe'],
          ALLOWED_ATTR: ['width', 'height', 'src', 'title', 'frameborder', 'allow', 'allowfullscreen'],
          ALLOWED_URI_REGEXP: /^https?:\/\/(www\.)?(youtube\.com|youtu\.be)/i,
        });
        setSanitizedDescription(sanitized);
      });
    }
  }, [heroDescription]);
  
  return (
    <>
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <div className={styles.heroBody}>
            <p className={styles.heroHeading}>{heroHeading}</p>
        </div>
      </div>
    </header>
    <main>
        <div className={styles.heroDescription}
          dangerouslySetInnerHTML={{ __html: sanitizedDescription }}
        />
    </main>
  </>
    
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="ICICLE AI Institute.">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
