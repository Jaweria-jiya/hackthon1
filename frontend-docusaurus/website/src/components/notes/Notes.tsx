import React from 'react';
import styles from './Notes.module.css';

const Notes = () => {
    return (
        <div className={styles.notesContainer}>
            <h2>My Notes</h2>
            <p>Note-taking is currently unavailable.</p>
        </div>
    );
};

export default Notes;