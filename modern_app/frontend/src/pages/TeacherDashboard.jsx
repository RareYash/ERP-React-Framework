import { useState, useEffect, useCallback } from "react";
import {
    fetchStudents, fetchStudent, fetchStudentSummary,
    fetchIndividualReviews, addReview, sentimentPreview,
    fetchClassAnalytics, updateStudentDetails,
} from "../services/api";
import Navbar from "../components/Navbar";
import StudentModal from "../components/StudentModal";
import ChatWidget from "../components/ChatWidget";
import {
    BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid,
    ResponsiveContainer, PieChart, Pie, Cell, Legend,
} from "recharts";
import "./Dashboard.css";
import "./TeacherDashboard.css";

const PIE_COLORS = ["#10b981", "#6366f1", "#f59e0b", "#ef4444", "#8b5cf6"];

const LABEL_COLORS = {
    "Very Positive": "#10b981",
    Positive: "#34d399",
    Neutral: "#f59e0b",
    Negative: "#f87171",
    "Very Negative": "#ef4444",
};

function sentimentBadge(label) {
    if (label.includes("Positive")) return "badge-success";
    if (label.includes("Negative")) return "badge-danger";
    return "badge-warning";
}

export default function TeacherDashboard() {
    const [tab, setTab] = useState("students");
    const [students, setStudents] = useState([]);
    const [selectedStudent, setSelectedStudent] = useState(null);
    const [selectedSummary, setSelectedSummary] = useState(null);
    const [individualReviews, setIndividualReviews] = useState(null);
    const [analytics, setAnalytics] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    // Review form
    const [reviewText, setReviewText] = useState("");
    const [reviewStudentId, setReviewStudentId] = useState("");
    const [preview, setPreview] = useState(null);
    const [submitting, setSubmitting] = useState(false);
    const [statusMsg, setStatusMsg] = useState("");

    // Edit details
    const [editMode, setEditMode] = useState(false);
    const [editName, setEditName] = useState("");
    const [editGrade, setEditGrade] = useState("");
    const [editArchetype, setEditArchetype] = useState("");
    const [editSaving, setEditSaving] = useState(false);

    // Analytics drill-down
    const [drillDown, setDrillDown] = useState(null); // e.g. "Positive", "Neutral", "Negative", "all"

    // Modal
    const [showModal, setShowModal] = useState(false);

    // Search
    const [searchQuery, setSearchQuery] = useState("");

    const loadStudents = useCallback(async () => {
        try {
            const data = await fetchStudents();
            setStudents(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => { loadStudents(); }, [loadStudents]);

    async function loadAnalytics() {
        try {
            const data = await fetchClassAnalytics();
            setAnalytics(data);
        } catch (err) {
            setError(err.message);
        }
    }

    async function handleStudentClick(studentId, openModal = true) {
        try {
            const [stu, sum, revs] = await Promise.all([
                fetchStudent(studentId),
                fetchStudentSummary(studentId),
                fetchIndividualReviews(studentId),
            ]);
            setSelectedStudent(stu);
            setSelectedSummary(sum);
            setIndividualReviews(revs);
            setReviewStudentId(studentId);
            setEditMode(false);
            if (openModal) setShowModal(true);
        } catch (err) {
            setError(err.message);
        }
    }

    function handleExpandFromModal() {
        setShowModal(false);
        // scroll to the detail panel
        setTimeout(() => {
            document.querySelector(".card")?.scrollIntoView({ behavior: "smooth" });
        }, 100);
    }

    async function handlePreview() {
        if (!reviewText.trim()) return;
        try {
            const result = await sentimentPreview(reviewText);
            setPreview(result);
        } catch (err) {
            setError(err.message);
        }
    }

    async function handleSubmitReview(e) {
        e.preventDefault();
        if (!reviewStudentId || !reviewText.trim()) return;
        setSubmitting(true);
        setStatusMsg("");
        try {
            await addReview(reviewStudentId, reviewText, "Teacher");
            setStatusMsg("Review added successfully!");
            setReviewText("");
            setPreview(null);
            await handleStudentClick(reviewStudentId);
        } catch (err) {
            setStatusMsg(`Error: ${err.message}`);
        } finally {
            setSubmitting(false);
        }
    }

    function startEditMode() {
        setEditName(selectedStudent["Student Name"]);
        setEditGrade(selectedStudent["Grade"]);
        setEditArchetype(selectedStudent["Archetype"]);
        setEditMode(true);
    }

    async function handleSaveDetails() {
        setEditSaving(true);
        try {
            await updateStudentDetails(selectedStudent["Student Number"], {
                name: editName,
                grade: editGrade,
                archetype: editArchetype,
            });
            await handleStudentClick(selectedStudent["Student Number"]);
            await loadStudents(); // refresh list
            setEditMode(false);
        } catch (err) {
            setError(err.message);
        } finally {
            setEditSaving(false);
        }
    }

    function handleTabChange(newTab) {
        setTab(newTab);
        if (newTab === "analytics" && !analytics) loadAnalytics();
    }

    // Build drill-down list from analytics data
    function getDrillDownStudents() {
        if (!analytics || !analytics.student_sentiments) return [];
        const list = analytics.student_sentiments;
        if (drillDown === "all") return list;
        if (drillDown === "Positive") return list.filter((s) => s.label === "Positive" || s.label === "Very Positive");
        if (drillDown === "Needs Attention") return list.filter((s) => s.label === "Negative" || s.label === "Very Negative");
        return list.filter((s) => s.label === drillDown);
    }

    const filteredStudents = students.filter(
        (s) => s.name.toLowerCase().includes(searchQuery.toLowerCase()) || s.id.includes(searchQuery)
    );

    if (loading) {
        return (
            <>
                <Navbar />
                <div className="dashboard">
                    <div className="loading-state"><div className="spinner" /><p>Loading students…</p></div>
                </div>
            </>
        );
    }

    return (
        <>
            <Navbar />
            <div className="dashboard animate-fade-in">
                <div className="dashboard-header">
                    <h1>Teacher <span className="text-gradient">Dashboard</span></h1>
                    <p>Manage reviews, edit student details, and view analytics</p>
                </div>

                {/* Tabs */}
                <div className="dashboard-tabs">
                    {["students", "review", "analytics"].map((t) => (
                        <button key={t} className={`tab-btn ${tab === t ? "active" : ""}`} onClick={() => handleTabChange(t)}>
                            {t === "students" ? "👥 Students" : t === "review" ? "✏️ Add Review" : "📊 Analytics"}
                        </button>
                    ))}
                </div>

                {error && <div className="alert alert-danger">❌ {error}</div>}

                {/* ====== STUDENTS TAB ====== */}
                {tab === "students" && (
                    <>
                        <div className="filter-bar">
                            <input className="form-input" type="text" placeholder="🔍 Search by name or ID…" value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} />
                            <span className="text-muted" style={{ fontSize: "0.85rem" }}>{filteredStudents.length} students</span>
                        </div>

                        <div className="student-table-container">
                            <table className="student-table">
                                <thead><tr><th>ID</th><th>Student Name</th><th>Actions</th></tr></thead>
                                <tbody>
                                    {filteredStudents.map((s) => (
                                        <tr key={s.id}>
                                            <td>{s.id}</td>
                                            <td>{s.name}</td>
                                            <td><button className="btn btn-sm btn-secondary" onClick={() => handleStudentClick(s.id, true)}>👁️ View</button></td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>

                        {/* ==== Student Detail Panel ==== */}
                        {selectedStudent && selectedSummary && (
                            <div className="card" style={{ marginBottom: "var(--space-xl)" }}>
                                {/* Header — View / Edit toggle */}
                                {!editMode ? (
                                    <>
                                        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "var(--space-md)" }}>
                                            <h3>
                                                {selectedStudent["Student Name"]} — Grade {selectedStudent["Grade"]}
                                                <span className="badge badge-info" style={{ marginLeft: "0.5rem" }}>{selectedStudent["Archetype"]}</span>
                                            </h3>
                                            <button className="btn btn-sm btn-primary" onClick={startEditMode}>✏️ Edit Details</button>
                                        </div>
                                    </>
                                ) : (
                                    <div className="review-form-card" style={{ marginBottom: "var(--space-md)" }}>
                                        <h3>✏️ Edit Student Details</h3>
                                        <div className="form-group">
                                            <label className="form-label">Name</label>
                                            <input className="form-input" value={editName} onChange={(e) => setEditName(e.target.value)} />
                                        </div>
                                        <div className="form-group">
                                            <label className="form-label">Grade</label>
                                            <input className="form-input" value={editGrade} onChange={(e) => setEditGrade(e.target.value)} />
                                        </div>
                                        <div className="form-group">
                                            <label className="form-label">Archetype</label>
                                            <input className="form-input" value={editArchetype} onChange={(e) => setEditArchetype(e.target.value)} />
                                        </div>
                                        <div className="review-form-actions">
                                            <button className="btn btn-success btn-sm" onClick={handleSaveDetails} disabled={editSaving}>
                                                {editSaving ? "Saving…" : "💾 Save"}
                                            </button>
                                            <button className="btn btn-secondary btn-sm" onClick={() => setEditMode(false)}>Cancel</button>
                                        </div>
                                    </div>
                                )}

                                {/* Metrics Row */}
                                <div className="metrics-row" style={{ marginBottom: "var(--space-lg)" }}>
                                    <div className="metric-card info">
                                        <span className="metric-card-icon">🎯</span>
                                        <span className="metric-card-value">{(selectedSummary.overall_sentiment.compound * 100).toFixed(0)}%</span>
                                        <span className="metric-card-label">Sentiment</span>
                                    </div>
                                    <div className="metric-card positive">
                                        <span className="metric-card-icon">💪</span>
                                        <span className="metric-card-value">{selectedSummary.strengths?.length || 0}</span>
                                        <span className="metric-card-label">Strengths</span>
                                    </div>
                                    <div className="metric-card neutral">
                                        <span className="metric-card-icon">📈</span>
                                        <span className="metric-card-value">{selectedSummary.improvements?.length || 0}</span>
                                        <span className="metric-card-label">Improvements</span>
                                    </div>
                                    {individualReviews && (
                                        <div className="metric-card info">
                                            <span className="metric-card-icon">📊</span>
                                            <span className="metric-card-value">{individualReviews.final_score.label}</span>
                                            <span className="metric-card-label">Final Score ({individualReviews.final_score.total_reviews} reviews)</span>
                                        </div>
                                    )}
                                </div>

                                {/* Individual Review Timeline */}
                                {individualReviews && individualReviews.reviews.length > 0 && (
                                    <div style={{ marginBottom: "var(--space-lg)" }}>
                                        <h3 style={{ marginBottom: "var(--space-md)" }}>📋 Review Timeline</h3>
                                        <div className="review-timeline">
                                            {individualReviews.reviews.map((rev, i) => (
                                                <div key={i} className="timeline-item">
                                                    <div className="timeline-header">
                                                        <span className="timeline-date">{rev.date}</span>
                                                        <span className="timeline-teacher">{rev.teacher}</span>
                                                        <span className={`badge ${sentimentBadge(rev.sentiment.label)}`}>
                                                            {rev.sentiment.label} ({(rev.sentiment.compound * 100).toFixed(0)}%)
                                                        </span>
                                                    </div>
                                                    <div className="timeline-text">{rev.text}</div>
                                                </div>
                                            ))}
                                        </div>

                                        {/* Final Collective Score */}
                                        <div className="sentiment-preview" style={{ marginTop: "var(--space-md)" }}>
                                            <div>
                                                <strong>📊 Collective Final Score: </strong>
                                                <span className="sentiment-preview-score">{(individualReviews.final_score.compound * 100).toFixed(0)}%</span>
                                                <span className={`badge ${sentimentBadge(individualReviews.final_score.label)}`} style={{ marginLeft: "0.5rem" }}>
                                                    {individualReviews.final_score.label}
                                                </span>
                                            </div>
                                            <span style={{ fontSize: "0.85rem", color: "var(--color-text-secondary)" }}>
                                                Based on {individualReviews.final_score.total_reviews} review(s)
                                            </span>
                                        </div>
                                    </div>
                                )}

                                <button className="btn btn-primary btn-sm" onClick={() => { setReviewStudentId(selectedStudent["Student Number"]); setTab("review"); }}>
                                    ✏️ Add Review for this Student
                                </button>
                            </div>
                        )}
                    </>
                )}

                {/* ====== ADD REVIEW TAB ====== */}
                {tab === "review" && (
                    <div className="review-form-card">
                        <h3>✏️ Add a Review</h3>
                        {statusMsg && (
                            <div className={`status-message ${statusMsg.startsWith("Error") ? "alert alert-danger" : "alert alert-success"}`}>{statusMsg}</div>
                        )}
                        <form onSubmit={handleSubmitReview}>
                            <div className="form-group">
                                <label className="form-label">Student</label>
                                <select className="form-select" value={reviewStudentId} onChange={(e) => setReviewStudentId(e.target.value)} required>
                                    <option value="">Select a student…</option>
                                    {students.map((s) => (<option key={s.id} value={s.id}>{s.name} ({s.id})</option>))}
                                </select>
                            </div>
                            <div className="form-group">
                                <label className="form-label">Review</label>
                                <textarea className="form-textarea" placeholder="Write your review here…" value={reviewText} onChange={(e) => setReviewText(e.target.value)} required />
                            </div>
                            {preview && (
                                <div className="sentiment-preview">
                                    <div>
                                        <span className="sentiment-preview-score">{(preview.compound * 100).toFixed(0)}%</span>
                                        <span className={`badge ${sentimentBadge(preview.label)}`} style={{ marginLeft: "0.5rem" }}>{preview.label}</span>
                                    </div>
                                    <div className="sentiment-preview-details">
                                        <span>🎯 Adjusted: {(preview.compound * 100).toFixed(0)}%</span>
                                        <span>📊 Raw: {(preview.raw_score * 100).toFixed(0)}%</span>
                                        {preview.has_contrast && <span>⚖️ Mixed Sentiment</span>}
                                    </div>
                                </div>
                            )}
                            <div className="review-form-actions">
                                <button type="button" className="btn btn-secondary" onClick={handlePreview} disabled={!reviewText.trim()}>🔍 Preview Sentiment</button>
                                <button type="submit" className="btn btn-success" disabled={submitting || !reviewStudentId || !reviewText.trim()}>
                                    {submitting ? "Submitting…" : "✅ Submit Review"}
                                </button>
                            </div>
                        </form>
                    </div>
                )}

                {/* ====== ANALYTICS TAB ====== */}
                {tab === "analytics" && analytics && (
                    <>
                        {/* Clickable Metric Cards */}
                        <div className="metrics-row">
                            <div className={`metric-card info clickable-card ${drillDown === "all" ? "card-active" : ""}`} onClick={() => setDrillDown(drillDown === "all" ? null : "all")}>
                                <span className="metric-card-icon">👥</span>
                                <span className="metric-card-value">{analytics.total_students}</span>
                                <span className="metric-card-label">Total Students — Click to view all</span>
                            </div>
                            <div className={`metric-card positive clickable-card ${drillDown === "Positive" ? "card-active" : ""}`} onClick={() => setDrillDown(drillDown === "Positive" ? null : "Positive")}>
                                <span className="metric-card-icon">😊</span>
                                <span className="metric-card-value">{(analytics.label_counts["Positive"] || 0) + (analytics.label_counts["Very Positive"] || 0)}</span>
                                <span className="metric-card-label">Positive — Click for list</span>
                            </div>
                            <div className={`metric-card neutral clickable-card ${drillDown === "Neutral" ? "card-active" : ""}`} onClick={() => setDrillDown(drillDown === "Neutral" ? null : "Neutral")}>
                                <span className="metric-card-icon">😐</span>
                                <span className="metric-card-value">{analytics.label_counts["Neutral"] || 0}</span>
                                <span className="metric-card-label">Neutral — Click for list</span>
                            </div>
                            <div className={`metric-card negative clickable-card ${drillDown === "Needs Attention" ? "card-active" : ""}`} onClick={() => setDrillDown(drillDown === "Needs Attention" ? null : "Needs Attention")}>
                                <span className="metric-card-icon">😟</span>
                                <span className="metric-card-value">{(analytics.label_counts["Negative"] || 0) + (analytics.label_counts["Very Negative"] || 0)}</span>
                                <span className="metric-card-label">Needs Attention — Click for list</span>
                            </div>
                        </div>

                        {/* Drill-Down Panel */}
                        {drillDown && analytics.student_sentiments && (
                            <div className="card" style={{ marginBottom: "var(--space-2xl)" }}>
                                <h3 style={{ marginBottom: "var(--space-md)" }}>
                                    {drillDown === "all" ? "📋 All Students" : `📋 ${drillDown} Students`}
                                    <button className="btn btn-sm btn-secondary" style={{ marginLeft: "1rem" }} onClick={() => setDrillDown(null)}>✕ Close</button>
                                </h3>
                                <div className="student-table-container">
                                    <table className="student-table">
                                        <thead><tr><th>ID</th><th>Name</th><th>Score</th><th>Sentiment</th></tr></thead>
                                        <tbody>
                                            {getDrillDownStudents().map((s) => (
                                                <tr key={s.id}>
                                                    <td>{s.id}</td>
                                                    <td>{s.name}</td>
                                                    <td>{(s.compound * 100).toFixed(0)}%</td>
                                                    <td><span className={`badge ${sentimentBadge(s.label)}`}>{s.label}</span></td>
                                                </tr>
                                            ))}
                                            {getDrillDownStudents().length === 0 && (
                                                <tr><td colSpan={4} style={{ textAlign: "center", color: "var(--color-text-muted)" }}>No students in this category</td></tr>
                                            )}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        )}

                        <div className="charts-row">
                            <div className="chart-card">
                                <h3>📊 Sentiment Distribution</h3>
                                <ResponsiveContainer width="100%" height={300}>
                                    <PieChart>
                                        <Pie data={Object.entries(analytics.label_counts).map(([name, value]) => ({ name, value }))} cx="50%" cy="50%" innerRadius={60} outerRadius={100} dataKey="value" label>
                                            {Object.entries(analytics.label_counts).map(([name], i) => (
                                                <Cell key={i} fill={LABEL_COLORS[name] || PIE_COLORS[i % PIE_COLORS.length]} />
                                            ))}
                                        </Pie>
                                        <Tooltip contentStyle={{ background: "#1e293b", border: "1px solid #334155", borderRadius: 8, color: "#f1f5f9" }} />
                                        <Legend wrapperStyle={{ color: "#94a3b8", fontSize: 12 }} />
                                    </PieChart>
                                </ResponsiveContainer>
                            </div>
                            <div className="chart-card">
                                <h3>📈 Student Archetypes</h3>
                                <ResponsiveContainer width="100%" height={300}>
                                    <BarChart data={Object.entries(analytics.archetype_counts).map(([name, count]) => ({ name, count }))}>
                                        <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                                        <XAxis dataKey="name" tick={{ fill: "#94a3b8", fontSize: 11 }} angle={-20} textAnchor="end" height={60} />
                                        <YAxis tick={{ fill: "#94a3b8" }} />
                                        <Tooltip contentStyle={{ background: "#1e293b", border: "1px solid #334155", borderRadius: 8, color: "#f1f5f9" }} />
                                        <Bar dataKey="count" fill="#6366f1" radius={[6, 6, 0, 0]} />
                                    </BarChart>
                                </ResponsiveContainer>
                            </div>
                        </div>

                        {/* Sentiment Dist Bars */}
                        <div className="card" style={{ marginBottom: "var(--space-2xl)" }}>
                            <h3 style={{ marginBottom: "var(--space-lg)" }}>📊 Detailed Distribution</h3>
                            <div className="sentiment-dist">
                                {Object.entries(analytics.label_counts).map(([label, count]) => (
                                    <div key={label} className="sentiment-dist-row">
                                        <span className="sentiment-dist-label">{label}</span>
                                        <div className="sentiment-dist-bar-bg">
                                            <div className="sentiment-dist-bar" style={{ width: `${(count / analytics.total_students) * 100}%`, background: LABEL_COLORS[label] || "#6366f1" }} />
                                        </div>
                                        <span className="sentiment-dist-count">{count}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </>
                )}

                {tab === "analytics" && !analytics && (
                    <div className="loading-state"><div className="spinner" /><p>Loading analytics…</p></div>
                )}
            </div>

            {/* Student Profile Modal */}
            {showModal && selectedStudent && (
                <StudentModal
                    student={selectedStudent}
                    summary={selectedSummary}
                    reviews={individualReviews}
                    onClose={() => setShowModal(false)}
                />
            )}

            {/* AI Chat Widget */}
            <ChatWidget />
        </>
    );
}
