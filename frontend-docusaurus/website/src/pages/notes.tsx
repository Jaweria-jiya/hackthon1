import React from 'react';
import Layout from '@theme/Layout';
import Notes from '@site/src/components/notes/Notes';

export default function NotesPage() {
    return (
        <Layout title="My Notes" description="Your personal notes for the book">
            <main>
                <Notes />
            </main>
        </Layout>
    );
}
