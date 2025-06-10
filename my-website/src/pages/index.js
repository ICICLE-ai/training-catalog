import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';

import Heading from '@theme/Heading';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  const { heroHeading, heroDescription } = siteConfig.customFields;
  return (
    <>
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <div className={clsx('container', styles.heroBody)}>
            <p className={styles.heroHeading}>{heroHeading}</p>
        </div>
      </div>
    </header>
    <main>
        <div className={clsx('container', styles.heroBody)}>
          <p className={styles.heroDescription}>{heroDescription}</p>
        </div>
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
