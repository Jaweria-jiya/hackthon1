import React from 'react';
import Layout from '@theme/Layout';
import Progress from '@site/src/components/progress/Progress';

export default function ProgressPage() {
    return (
        <Layout title="My Progress" description="Your progress through the book">
            <main>
                <Progress />
            </main>
        </Layout>
    );
}
