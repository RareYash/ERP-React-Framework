import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import { fetchStudent, fetchStudentSummary } from "../services/api";
import Navbar from "../components/Navbar";
import {
    RadarChart, Radar, PolarGrid, PolarAngleAxis,
    PolarRadiusAxis, ResponsiveContainer,
    BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, Cell,
} from "recharts";
import "./Dashboard.css";

const COLORS = ["#6366f1", "#8b5cf6", "#3b82f6", "#10b981", "#f59e0b"];

function getSentimentBadge(label) {
    const map = {
        "Very Positive": "success",
        "Positive": "success",
        "Neutral": "warning",
        "Negative": "danger",
        "Very Negative": "danger",
    };
    return map[label] || "info";
}

export default function ParentDashboard() {
    const { user } = useAuth();
    const [student, setStudent] = useState(null);
    const [summary, setSummary] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        async function load() {
            try {
                const sid = user.student_id;
                const [stu, sum] = await Promise.all([
                    fetchStudent(sid),
                    fetchStudentSummary(sid),
                ]);
                setStudent(stu);
                setSummary(sum);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }
        load();
    }, [user.student_id]);

    if (loading) {
        return (
            <>
                <Navbar />
                <div className="dashboard">
                    <div className="loading-state">
                        <div className="spinner" />
                        <p>Loading student data…</p>
                    </div>
                </div>
            </>
        );
    }

    if (error) {
        return (
            <>
                <Navbar />
                <div className="dashboard">
                    <div className="alert alert-danger">❌ {error}</div>
                </div>
            </>
        );
    }

    const sentiment = summary.overall_sentiment;
    const categories = summary.category_scores;
    const strengths = summary.strengths || [];
    const improvements = summary.improvements || [];

    // Prepare chart data
    const categoryData = Object.entries(categories).map(([name, score]) => ({
        category: name.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase()),
        score: Math.round(score * 100),
        fullMark: 100,
    }));

    const barData = Object.entries(categories).map(([name, score]) => ({
        name: name.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase()),
        score: Math.round(score * 100),
    }));

    function handleDownload() {
        const report = [
            `Student Report — ${student["Student Name"]}`,
            `Grade: ${student["Grade"]}`,
            `Archetype: ${student["Archetype"]}`,
            ``,
            `Overall Sentiment: ${sentiment.label} (${sentiment.compound.toFixed(2)})`,
            ``,
            `Category Scores:`,
            ...barData.map((d) => `  ${d.name}: ${d.score}%`),
            ``,
            `Strengths:`,
            ...strengths.map((s) => `  ✅ ${s}`),
            ``,
            `Areas for Improvement:`,
            ...improvements.map((i) => `  📈 ${i}`),
            ``,
            `Summary:`,
            summary.summary_text,
            ``,
            `Teacher Review:`,
            student["Teacher Review"],
        ].join("\n");

        const blob = new Blob([report], { type: "text/plain" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `report_${student["Student Name"].replace(/\s+/g, "_")}.txt`;
        a.click();
        URL.revokeObjectURL(url);
    }

    return (
        <>
            <Navbar />
            <div className="dashboard animate-fade-in">
                <div className="dashboard-header">
                    <h1>
                        {student["Student Name"]}&apos;s{" "}
                        <span className="text-gradient">Dashboard</span>
                    </h1>
                    <p>
                        Grade {student["Grade"]} · {student["Archetype"]}
                    </p>
                </div>

                {/* Download */}
                <div className="download-row">
                    <button className="btn btn-secondary" onClick={handleDownload}>
                        📥 Download Report
                    </button>
                </div>

                {/* Metrics */}
                <div className="metrics-row">
                    <div className={`metric-card ${getSentimentBadge(sentiment.label) === "success" ? "positive" : getSentimentBadge(sentiment.label) === "danger" ? "negative" : "neutral"}`}>
                        <span className="metric-card-icon">🎯</span>
                        <span className="metric-card-value">{(sentiment.compound * 100).toFixed(0)}%</span>
                        <span className="metric-card-label">Overall Sentiment</span>
                    </div>
                    <div className="metric-card positive">
                        <span className="metric-card-icon">😊</span>
                        <span className="metric-card-value">{(sentiment.pos * 100).toFixed(0)}%</span>
                        <span className="metric-card-label">Positive</span>
                    </div>
                    <div className="metric-card neutral">
                        <span className="metric-card-icon">😐</span>
                        <span className="metric-card-value">{(sentiment.neu * 100).toFixed(0)}%</span>
                        <span className="metric-card-label">Neutral</span>
                    </div>
                    <div className="metric-card negative">
                        <span className="metric-card-icon">😟</span>
                        <span className="metric-card-value">{(sentiment.neg * 100).toFixed(0)}%</span>
                        <span className="metric-card-label">Negative</span>
                    </div>
                </div>

                {/* Charts */}
                <div className="charts-row">
                    <div className="chart-card">
                        <h3>📊 Category Radar</h3>
                        <ResponsiveContainer width="100%" height={300}>
                            <RadarChart data={categoryData}>
                                <PolarGrid stroke="#334155" />
                                <PolarAngleAxis dataKey="category" tick={{ fill: "#94a3b8", fontSize: 12 }} />
                                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fill: "#64748b", fontSize: 10 }} />
                                <Radar
                                    dataKey="score"
                                    stroke="#6366f1"
                                    fill="#6366f1"
                                    fillOpacity={0.3}
                                />
                            </RadarChart>
                        </ResponsiveContainer>
                    </div>

                    <div className="chart-card">
                        <h3>📈 Category Breakdown</h3>
                        <ResponsiveContainer width="100%" height={300}>
                            <BarChart data={barData} layout="vertical">
                                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                                <XAxis type="number" domain={[0, 100]} tick={{ fill: "#94a3b8" }} />
                                <YAxis dataKey="name" type="category" width={120} tick={{ fill: "#94a3b8", fontSize: 11 }} />
                                <Tooltip contentStyle={{ background: "#1e293b", border: "1px solid #334155", borderRadius: 8, color: "#f1f5f9" }} />
                                <Bar dataKey="score" radius={[0, 6, 6, 0]}>
                                    {barData.map((_, i) => (
                                        <Cell key={i} fill={COLORS[i % COLORS.length]} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Strengths & Improvements */}
                <div className="insights-row">
                    <div className="insight-card">
                        <h3>✅ Strengths</h3>
                        <ul className="insight-list">
                            {strengths.length > 0 ? (
                                strengths.map((s, i) => (
                                    <li key={i} className="insight-item strength">{s}</li>
                                ))
                            ) : (
                                <li className="insight-item strength">No specific strengths identified yet</li>
                            )}
                        </ul>
                    </div>
                    <div className="insight-card">
                        <h3>📈 Areas for Improvement</h3>
                        <ul className="insight-list">
                            {improvements.length > 0 ? (
                                improvements.map((s, i) => (
                                    <li key={i} className="insight-item improvement">{s}</li>
                                ))
                            ) : (
                                <li className="insight-item improvement">No improvement areas identified</li>
                            )}
                        </ul>
                    </div>
                </div>

                {/* Summary */}
                <div className="summary-card">
                    <h3>📝 AI Summary</h3>
                    <div className="summary-text">{summary.summary_text}</div>
                </div>

                {/* Original Review */}
                <div className="review-section">
                    <h3>📋 Teacher&apos;s Review</h3>
                    <div className="review-content">{student["Teacher Review"]}</div>
                </div>
            </div>
        </>
    );
}
