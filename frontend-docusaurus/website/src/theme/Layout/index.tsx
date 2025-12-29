import React, {type ReactNode} from 'react';
import Layout from '@theme-original/Layout';
import type LayoutType from '@theme/Layout';
import type {WrapperProps} from '@docusaurus/types';
import Chatbot from '@site/src/components/chatbot/Chatbot'; // Import the Chatbot component

type Props = WrapperProps<typeof LayoutType>;

export default function LayoutWrapper(props: Props): ReactNode {
  return (
    <>
      <Layout {...props} />
      <Chatbot />
    </>
  );
}
