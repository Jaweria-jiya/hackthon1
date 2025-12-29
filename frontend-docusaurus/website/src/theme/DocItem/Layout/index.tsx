import React, {type ReactNode, useState, useEffect} from 'react';
import clsx from 'clsx';
import {useWindowSize, ThemeClassNames} from '@docusaurus/theme-common';
import {useDoc} from '@docusaurus/plugin-content-docs/client';
import DocItemPaginator from '@theme/DocItem/Paginator';
import DocVersionBanner from '@theme/DocVersionBanner';
import DocVersionBadge from '@theme/DocVersionBadge';
import DocItemFooter from '@theme/DocItem/Footer';
import DocItemTOCMobile from '@theme/DocItem/TOC/Mobile';
import DocItemTOCDesktop from '@theme/DocItem/TOC/Desktop';
import DocItemContent from '@theme/DocItem/Content';
import DocBreadcrumbs from '@theme/DocBreadcrumbs';
import ContentVisibility from '@theme/ContentVisibility';
import type {Props} from '@theme/DocItem/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import { useAuth } from '@site/src/contexts/AuthContext'; // Import useAuth


import styles from './styles.module.css';

/**
 * Decide if the toc should be rendered, on mobile or desktop viewports
 */
function useDocTOC() {
  const {frontMatter, toc} = useDoc();
  const windowSize = useWindowSize();

  const hidden = frontMatter.hide_table_of_contents;
  const canRender = !hidden && toc.length > 0;

  const mobile = canRender ? <DocItemTOCMobile /> : undefined;

  const desktop =
    canRender && (windowSize === 'desktop' || windowSize === 'ssr') ? (
      <DocItemTOCDesktop />
    ) : undefined;

  return {
    hidden,
    mobile,
    desktop,
  };
}

export default function DocItemLayout({children}: Props): ReactNode {
  const docTOC = useDocTOC();
  const {metadata} = useDoc();
  const { siteConfig } = useDocusaurusContext();
  const apiBaseUrl = siteConfig.customFields.apiBaseUrl as string;
  const { user } = useAuth(); // Get user from auth context

  const [buttonText, setButtonText] = useState('Translate to Urdu');
  const [buttonDisabled, setButtonDisabled] = useState(false);
  const [translatedContent, setTranslatedContent] = useState<string | null>(null);
  const [originalContent, setOriginalContent] = useState<string | null>(null);


  const handleTranslateToggle = async () => {
    if (!user) { // Check if user is authenticated
      window.location.href = '/signin';
      return;
    }

    // Track the activity
    try {
      await fetch(`${apiBaseUrl}/activity/track`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('mock_token')}`
        },
        body: JSON.stringify({
          user_id: user.id,
          email: user.email,
          action: 'translate_to_urdu',
          resource_id: metadata.id,
        }),
      });
    } catch (error) {
      console.error('Failed to track activity:', error);
    }

    // If content is already translated, revert to original
    if (translatedContent) {
      setTranslatedContent(null);
      setButtonText('Translate to Urdu');
      setOriginalContent(null); // Clear original content reference
      return;
    }

    const contentElement = document.querySelector('.markdown');
    if (!contentElement) {
      console.error('Content element not found for translation.');
      return;
    }

    setOriginalContent(contentElement.innerHTML); // Store original HTML
    setButtonDisabled(true);
    setButtonText('Translating...');

    try {
      const response = await fetch(`${apiBaseUrl}/translate/urdu`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: contentElement.innerHTML }),
      });

      if (!response.ok) {
        throw new Error('Translation API request failed');
      }

      const data = await response.json();
      setTranslatedContent(data.translated_content);
      setButtonText('View Original');
    } catch (error) {
      console.error('Translation failed:', error);
      alert('Translation failed. Please try again.');
      setTranslatedContent(null); // Clear translated content
      setButtonText('Translate to Urdu');
    } finally {
      setButtonDisabled(false);
    }
  };


  return (
    <div className="row">
      <div className={clsx('col', !docTOC.hidden && styles.docItemCol)}>
        <ContentVisibility metadata={metadata} />
        <DocVersionBanner />
        <div className={styles.docItemContainer}>
          <article>
            <div className={styles.docBreadcrumbsAndTranslate}>
              <DocBreadcrumbs />
              {metadata.title && ( // Only show button if there's a title
                <button
                  className="button button--secondary button--sm"
                  style={{ marginLeft: '1rem', verticalAlign: 'middle' }}
                  onClick={handleTranslateToggle}
                  disabled={buttonDisabled}>
                  {buttonText}
                </button>
              )}
            </div>
            <DocVersionBadge />
            {docTOC.mobile}
            {translatedContent ? (
              <div
                className={clsx(ThemeClassNames.docs.docMarkdown, 'markdown')}
                dangerouslySetInnerHTML={{ __html: translatedContent }}
              />
            ) : (
              <DocItemContent>{children}</DocItemContent>
            )}
            <DocItemFooter />
          </article>
          <DocItemPaginator />
        </div>
      </div>
      {docTOC.desktop && <div className="col col--3">{docTOC.desktop}</div>}
    </div>
  );
}
