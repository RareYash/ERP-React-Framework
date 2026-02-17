import { useEffect, useRef } from "react";
import "./StudentModal.css";

function sentimentBadge(label) {
    if (!label) return "badge-info";
    if (label.includes("Positive")) return "badge-success";
    if (label.includes("Negative")) return "badge-danger";
    return "badge-warning";
}

function avatarUrl(name) {
    // DiceBear Adventurer style — unique avatars from student name
    return `https://api.dicebear.com/9.x/adventurer/svg?seed=${encodeURIComponent(name)}&backgroundColor=b6e3f4,c0aede,d1d4f9&radius=50`;
}

export default function StudentModal({ student, summary, reviews, onClose }) {
    const overlayRef = useRef(null);

    useEffect(() => {
        function handleKey(e) {
            if (e.key === "Escape") onClose();
        }
        document.addEventListener("keydown", handleKey);
        return () => document.removeEventListener("keydown", handleKey);
    }, [onClose]);

    function handleOverlayClick(e) {
        if (e.target === overlayRef.current) onClose();
    }

    if (!student) return null;

    const name = student["Student Name"];
    const id = student["Student Number"];
    const grade = student["Grade"];
    const archetype = student["Archetype"];
    const compound = summary?.overall_sentiment?.compound ?? 0;
    const label = summary?.overall_sentiment?.label ?? "N/A";
    const finalScore = reviews?.final_score;

    return (
        <div className="modal-overlay" ref={overlayRef} onClick={handleOverlayClick}>
            <div className="modal-content animate-scale-in">
                {/* Close Button */}
                <button className="modal-close" onClick={onClose} aria-label="Close">✕</button>

                {/* Profile Header */}
                <div className="modal-profile-header">
                    <img className="modal-avatar" src={avatarUrl(name)} alt={name} />
                    <h2 className="modal-name">{name}</h2>
                    <span className="modal-id">ID: {id}</span>
                </div>

                {/* Info Cards */}
                <div className="modal-info-grid">
                    <div className="modal-info-card">
                        <span className="modal-info-icon">🎓</span>
                        <span className="modal-info-label">Grade</span>
                        <span className="modal-info-value">{grade}</span>
                    </div>
                    <div className="modal-info-card">
                        <span className="modal-info-icon">🧬</span>
                        <span className="modal-info-label">Archetype</span>
                        <span className="modal-info-value">{archetype}</span>
                    </div>
                    <div className="modal-info-card">
                        <span className="modal-info-icon">🎯</span>
                        <span className="modal-info-label">Sentiment</span>
                        <span className="modal-info-value">
                            <span className={`badge ${sentimentBadge(label)}`}>{label}</span>
                        </span>
                    </div>
                    <div className="modal-info-card">
                        <span className="modal-info-icon">📊</span>
                        <span className="modal-info-label">Score</span>
                        <span className="modal-info-value score-value">{(compound * 100).toFixed(0)}%</span>
                    </div>
                </div>

                {/* Final score from individual reviews */}
                {finalScore && (
                    <div className="modal-final-score">
                        <span>Collective Final Score</span>
                        <div>
                            <span className="modal-final-score-value">{(finalScore.compound * 100).toFixed(0)}%</span>
                            <span className={`badge ${sentimentBadge(finalScore.label)}`} style={{ marginLeft: "0.5rem" }}>{finalScore.label}</span>
                        </div>
                        <span className="modal-reviews-count">{finalScore.total_reviews} review(s)</span>
                    </div>
                )}

                {/* Strengths & Improvements */}
                {summary && (
                    <div className="modal-tags-section">
                        {summary.strengths?.length > 0 && (
                            <div className="modal-tags-group">
                                <h4>💪 Strengths</h4>
                                <div className="modal-tags">
                                    {summary.strengths.slice(0, 5).map((s, i) => (
                                        <span key={i} className="modal-tag tag-positive">{s}</span>
                                    ))}
                                </div>
                            </div>
                        )}
                        {summary.improvements?.length > 0 && (
                            <div className="modal-tags-group">
                                <h4>📈 Improvements</h4>
                                <div className="modal-tags">
                                    {summary.improvements.slice(0, 5).map((s, i) => (
                                        <span key={i} className="modal-tag tag-neutral">{s}</span>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}
