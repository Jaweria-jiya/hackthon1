import type {ReactNode} from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext'; // Still needed if siteConfig.title or tagline might be used elsewhere, though not for hardcoded title.
import Heading from '@theme/Heading';

import styles from './index.module.css';



// Custom Home component without Layout, directly rendering fullscreen content
export default function Home(): ReactNode {
  // const {siteConfig} = useDocusaurusContext(); // Not needed as title and tagline are hardcoded

  return (
    <div className={styles.fullPageWrapper}> {/* Full page wrapper for background and centering */}
      <div className={styles.mainContentArea}> {/* Area to center main heading and CTA */}
        <Heading as="h1" className={styles.mainHeading}>
          Physical AI & Humanoid Robotics
        </Heading>
        <p className={styles.subHeading}>
          An AI-native textbook on robotics
        </p>
        <Link
          className={styles.startReadingLink}
          to="/docs/intro">
          Start Reading →
        </Link>
      </div>

    </div>
  );
}