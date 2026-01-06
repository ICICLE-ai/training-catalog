import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import DOMPurify from 'isomorphic-dompurify';

import Heading from '@theme/Heading';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  const { heroHeading, heroDescription } = siteConfig.customFields;
  
  // Sanitize HTML to prevent XSS attacks
  const sanitizedDescription = DOMPurify.sanitize(heroDescription, {
    ALLOWED_TAGS: ['p', 'br', 'b', 'strong', 'iframe'],
    ALLOWED_ATTR: ['width', 'height', 'src', 'title', 'frameborder', 'allow', 'allowfullscreen'],
    ALLOWED_URI_REGEXP: /^https?:\/\/(www\.)?(youtube\.com|youtu\.be)/i,
  });
  
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
