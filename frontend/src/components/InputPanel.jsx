import React, { useState } from 'react';
import axios from 'axios';
import { ChevronDown, ChevronUp, Sliders, MapPin, Activity, Link2, Loader2, CheckCircle, XCircle } from 'lucide-react';

const InputPanel = ({ signals, context, setSignals, setContext, language, onSourceVerified }) => {
    const [openSection, setOpenSection] = useState('context');
    const [proofDocs, setProofDocs] = useState({
        work_photos: false, training_certificate: false, upi_screenshot: false, business_license: false
    });
    const [businessInfo, setBusinessInfo] = useState({
        monthly_customers: '', income_range: '', business_name: '', platform_presence: ''
    });
    const [verifying, setVerifying] = useState(false);
    const [verification, setVerification] = useState(null);

    const handleChange = (e, field, type = 'signals') => {
        const val = e.target.type === 'number' ? parseFloat(e.target.value) : e.target.value;
        if (type === 'signals') setSignals(prev => ({ ...prev, [field]: val }));
        else setContext(prev => ({ ...prev, [field]: val }));
    };

    const handleDocToggle = (key) => {
        setProofDocs(prev => ({ ...prev, [key]: !prev[key] }));
    };

    const handleBusinessChange = (field, value) => {
        setBusinessInfo(prev => ({ ...prev, [field]: value }));
    };

    const verifySources = async () => {
        setVerifying(true);
        try {
            const res = await axios.post('/api/verify-sources', {
                documents: proofDocs,
                business_info: businessInfo
            });
            setVerification(res.data);
            if (onSourceVerified) onSourceVerified(res.data);
        } catch (e) {
            console.error('Work verification failed:', e);
        }
        setVerifying(false);
    };

    const runDemoScenario = () => {
        setContext({
            state: 'Bihar', area_type: 'Rural', opportunity_level: 'Low',
            infrastructure_access: 'Minimal', digital_access: 'Limited', domain: 'Agriculture & Allied'
        });
        setSignals({
            creation_output: 55, learning_behavior: 60, experience_consistency: 75,
            economic_activity: 35, innovation_problem_solving: 55, collaboration_community: 75,
            offline_capability: 92, digital_presence: 10,
            land_size_acres: 5, crop_diversity: 4, annual_yield_score: 92,
            training_completed: 3, income_stability: 3
        });
    };

    const runDemoScenarioUrban = () => {
        setContext({
            state: 'Karnataka', area_type: 'Urban', opportunity_level: 'High',
            infrastructure_access: 'High', digital_access: 'Regular', domain: 'Technology & IT'
        });
        setSignals({
            creation_output: 85, learning_behavior: 90, experience_consistency: 80,
            economic_activity: 65, innovation_problem_solving: 85, collaboration_community: 80,
            offline_capability: 30, digital_presence: 95,
            years_experience: 5, portfolio_items: 12, training_completed: 8,
            income_stability: 4
        });
    };

    const sections = [
        {
            id: 'context',
            title: language === 'en' ? 'User Context & Environment' : 'उपयोगकर्ता संदर्भ',
            icon: MapPin,
            content: (
                <div className="grid grid-cols-2 gap-4">
                    <div className="col-span-2 border-b border-gray-800 pb-4 mb-2">
                        <label className="text-xs text-accent block mb-1 font-bold uppercase tracking-wider">Primary Domain</label>
                        <select
                            value={context.domain || 'Retail & Sales'}
                            onChange={(e) => handleChange(e, 'domain', 'context')}
                            className="w-full bg-gray-900 border border-gray-700 rounded p-2 text-sm text-white focus:border-accent outline-none font-medium"
                        >
                            <option>Retail & Sales</option>
                            <option>Manufacturing & Operations</option>
                            <option>Logistics & Delivery</option>
                            <option>Agriculture & Allied</option>
                            <option>Construction & Skilled Trades</option>
                            <option>Education & Training</option>
                            <option>Business & Administration</option>
                            <option>Creative & Media</option>
                            <option>Service Industry</option>
                            <option>Entrepreneurship</option>
                        </select>
                    </div>

                    <div>
                        <label className="text-xs text-gray-500 block mb-1">State / Province</label>
                        <select
                            value={context.state}
                            onChange={(e) => handleChange(e, 'state', 'context')}
                            className="w-full bg-gray-900 border border-gray-700 rounded p-2 text-sm text-white focus:border-accent outline-none"
                        >
                            <option>Maharashtra</option><option>Karnataka</option><option>Delhi</option>
                            <option>Uttar Pradesh</option><option>Bihar</option><option>Tamil Nadu</option>
                            <option>West Bengal</option><option>Telangana</option><option>Odisha</option>
                            <option>Rajasthan</option><option>Kerala</option><option>Punjab</option>
                            <option>Haryana</option><option>Assam</option><option>Jharkhand</option>
                            <option>Chhattisgarh</option><option>Uttarakhand</option><option>Andhra Pradesh</option>
                            <option>Gujarat</option>
                        </select>
                    </div>
                    <div>
                        <label className="text-xs text-gray-500 block mb-1">Area Type</label>
                        <select
                            value={context.area_type}
                            onChange={(e) => handleChange(e, 'area_type', 'context')}
                            className="w-full bg-gray-900 border border-gray-700 rounded p-2 text-sm text-white focus:border-accent outline-none"
                        >
                            <option>Urban</option><option>Semi-Urban</option><option>Rural</option>
                        </select>
                    </div>
                    <div>
                        <label className="text-xs text-gray-500 block mb-1">Infrastructure Access</label>
                        <select
                            value={context.infrastructure_access}
                            onChange={(e) => handleChange(e, 'infrastructure_access', 'context')}
                            className="w-full bg-gray-900 border border-gray-700 rounded p-2 text-sm text-white focus:border-accent outline-none"
                        >
                            <option>High</option><option>Limited</option><option>Minimal</option>
                        </select>
                    </div>
                    <div>
                        <label className="text-xs text-gray-500 block mb-1">Digital Access</label>
                        <select
                            value={context.digital_access}
                            onChange={(e) => handleChange(e, 'digital_access', 'context')}
                            className="w-full bg-gray-900 border border-gray-700 rounded p-2 text-sm text-white focus:border-accent outline-none"
                        >
                            <option>Regular</option><option>Limited</option><option>Occasional</option>
                        </select>
                    </div>
                </div>
            )
        },
        {
            id: 'dimensions',
            title: language === 'en' ? 'Behavioral Dimensions' : 'व्यवहार आयाम',
            icon: Activity,
            content: (() => {
                // ── Structured Questions → Score Mapping ──
                const DIMENSION_QUESTIONS = [
                    {
                        key: 'learning_behavior',
                        label: 'Weekly Learning Hours',
                        question: 'How many hours do you spend learning new skills per week?',
                        options: [
                            { label: 'Less than 2 hours', value: 20 },
                            { label: '3–5 hours', value: 40 },
                            { label: '6–10 hours', value: 60 },
                            { label: '11–20 hours', value: 80 },
                            { label: '20+ hours', value: 95 }
                        ]
                    },
                    {
                        key: 'creation_output',
                        label: 'Projects Completed',
                        question: 'How many projects have you completed in the last 6 months?',
                        options: [
                            { label: 'None', value: 10 },
                            { label: '1–2 projects', value: 30 },
                            { label: '3–5 projects', value: 55 },
                            { label: '6–10 projects', value: 75 },
                            { label: '10+ projects', value: 90 }
                        ]
                    },
                    {
                        key: 'innovation_problem_solving',
                        label: 'Innovation & Problem Solving',
                        question: 'Have you participated in hackathons or proposed new ideas?',
                        options: [
                            { label: 'Never', value: 15 },
                            { label: 'Once or twice', value: 35 },
                            { label: 'A few times', value: 55 },
                            { label: 'Regularly', value: 75 },
                            { label: 'Frequently, with awards', value: 92 }
                        ]
                    },
                    {
                        key: 'digital_presence',
                        label: 'Digital Presence',
                        question: 'Which best describes your online presence?',
                        options: [
                            { label: 'No online presence', value: 10 },
                            { label: 'Basic social media only', value: 25 },
                            { label: 'LinkedIn profile active', value: 45 },
                            { label: 'GitHub or Portfolio site', value: 65 },
                            { label: 'GitHub + Portfolio + active posts', value: 85 }
                        ]
                    },
                    {
                        key: 'economic_activity',
                        label: 'Economic Activity',
                        question: 'What is your current work status?',
                        options: [
                            { label: 'Unemployed / Student (no work)', value: 15 },
                            { label: 'Part-time or gig work', value: 35 },
                            { label: 'Internship / Apprenticeship', value: 50 },
                            { label: 'Freelancing regularly', value: 65 },
                            { label: 'Full-time employed or business owner', value: 85 }
                        ]
                    },
                    {
                        key: 'collaboration_community',
                        label: 'Collaboration & Community',
                        question: 'How many team projects / open-source contributions?',
                        options: [
                            { label: 'None', value: 15 },
                            { label: '1–2 collaborations', value: 35 },
                            { label: '3–5 collaborations', value: 55 },
                            { label: '6–10 with active community roles', value: 75 },
                            { label: '10+ and mentoring others', value: 90 }
                        ]
                    },
                    {
                        key: 'experience_consistency',
                        label: 'Experience Consistency',
                        question: 'How consistent is your skill-building over the past year?',
                        options: [
                            { label: 'Very inconsistent / long gaps', value: 20 },
                            { label: 'Occasional bursts of activity', value: 40 },
                            { label: 'Moderate—learning some months', value: 55 },
                            { label: 'Consistent monthly effort', value: 75 },
                            { label: 'Daily / near-daily practice', value: 92 }
                        ]
                    },
                    {
                        key: 'offline_capability',
                        label: 'Offline / Practical Capability',
                        question: 'Can you perform your skills without internet access?',
                        options: [
                            { label: 'Fully dependent on internet', value: 20 },
                            { label: 'Mostly online-dependent', value: 40 },
                            { label: 'Mixed—some offline capability', value: 55 },
                            { label: 'Strong offline skills', value: 75 },
                            { label: 'Fully capable offline (hands-on trade)', value: 92 }
                        ]
                    }
                ];

                const handleSelect = (key, val) => {
                    setSignals(prev => ({ ...prev, [key]: Number(val) }));
                };

                const getBarColor = (v) => v >= 70 ? 'bg-emerald-500' : v >= 40 ? 'bg-amber-500' : 'bg-red-500';
                const getTextColor = (v) => v >= 70 ? 'text-emerald-400' : v >= 40 ? 'text-amber-400' : 'text-red-400';

                return (
                    <div className="space-y-4">
                        <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-blue-500/10 border border-blue-500/20 mb-1">
                            <Activity className="w-3.5 h-3.5 text-blue-400 shrink-0" />
                            <span className="text-[11px] text-blue-300">Scores are automatically derived from your activity data.</span>
                        </div>
                        {DIMENSION_QUESTIONS.map(q => {
                            const currentVal = signals[q.key] || 0;
                            return (
                                <div key={q.key} className="bg-gray-900/50 rounded-lg p-3 border border-gray-800">
                                    <div className="flex items-center justify-between mb-1.5">
                                        <label className="text-xs font-bold text-gray-300">{q.label}</label>
                                        <span className={`text-xs font-mono font-bold ${getTextColor(currentVal)}`}>{currentVal}</span>
                                    </div>
                                    <p className="text-[11px] text-gray-500 mb-2">{q.question}</p>
                                    <select
                                        value={currentVal}
                                        onChange={(e) => handleSelect(q.key, e.target.value)}
                                        className="w-full bg-gray-900 border border-gray-700 rounded p-2 text-sm text-white focus:border-accent outline-none"
                                    >
                                        <option value="0" disabled>Select an option…</option>
                                        {q.options.map((opt, i) => (
                                            <option key={i} value={opt.value}>{opt.label}</option>
                                        ))}
                                    </select>
                                    <div className="w-full bg-gray-800 rounded-full h-1 mt-2">
                                        <div className={`${getBarColor(currentVal)} h-1 rounded-full transition-all duration-500`} style={{ width: `${currentVal}%` }}></div>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                );
            })()
        },
        {
            id: 'signals',
            title: language === 'en' ? 'Work Domain & Activity' : 'कार्य डोमेन और गतिविधि',
            icon: Sliders,
            content: (
                <div className="space-y-4">
                    <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-blue-500/10 border border-blue-500/20 mb-1">
                        <Sliders className="w-3.5 h-3.5 text-blue-400 shrink-0" />
                        <span className="text-[11px] text-blue-300">Skill scores are calculated based on real work activity, not just technical skills.</span>
                    </div>
                    {(() => {
                        const domain = context.domain || 'Retail & Sales';
                        let fields = [];

                        if (domain === 'Retail & Sales') {
                            fields = [
                                { key: 'years_experience', label: 'Years of Experience', max: 40 },
                                { key: 'customers_served_monthly', label: 'Customers Served / Month', max: 5000 },
                                { key: 'products_sold_monthly', label: 'Products / Services Sold / Month', max: 1000 },
                                { key: 'training_completed', label: 'Training Programs Completed', max: 20 },
                                { key: 'income_stability', label: 'Income Stability (1=Irregular, 5=Very Stable)', max: 5 }
                            ];
                        } else if (domain === 'Manufacturing & Operations') {
                            fields = [
                                { key: 'years_experience', label: 'Years of Experience', max: 40 },
                                { key: 'units_produced_monthly', label: 'Units Produced / Month', max: 10000 },
                                { key: 'quality_score', label: 'Quality Rating (1-100)', max: 100 },
                                { key: 'training_completed', label: 'Safety / Skill Trainings Done', max: 20 },
                                { key: 'equipment_operated', label: 'Machines / Equipment Operated', max: 20 }
                            ];
                        } else if (domain === 'Logistics & Delivery') {
                            fields = [
                                { key: 'years_experience', label: 'Years of Experience', max: 30 },
                                { key: 'deliveries_monthly', label: 'Deliveries Completed / Month', max: 2000 },
                                { key: 'routes_managed', label: 'Routes / Areas Managed', max: 50 },
                                { key: 'on_time_percentage', label: 'On-Time Delivery % (0-100)', max: 100 },
                                { key: 'income_stability', label: 'Income Stability (1-5)', max: 5 }
                            ];
                        } else if (domain === 'Agriculture & Allied') {
                            fields = [
                                { key: 'land_size_acres', label: 'Land Size (Acres)', max: 50 },
                                { key: 'crop_diversity', label: 'Crop Types Grown', max: 10 },
                                { key: 'annual_yield_score', label: 'Annual Yield Score (0-100)', max: 100 },
                                { key: 'training_completed', label: 'Agri-Training Programs Done', max: 15 },
                                { key: 'income_stability', label: 'Income Stability (1-5)', max: 5 }
                            ];
                        } else if (domain === 'Construction & Skilled Trades') {
                            fields = [
                                { key: 'years_experience', label: 'Years of Experience', max: 40 },
                                { key: 'projects_completed', label: 'Projects / Sites Completed', max: 200 },
                                { key: 'certifications', label: 'Trade Certifications', max: 10 },
                                { key: 'tools_quality', label: 'Tools / Equipment Level (1=Basic, 5=Pro)', max: 5 },
                                { key: 'income_stability', label: 'Income Stability (1-5)', max: 5 }
                            ];
                        } else if (domain === 'Education & Training') {
                            fields = [
                                { key: 'teaching_years', label: 'Years Teaching / Training', max: 40 },
                                { key: 'students_impacted', label: 'Students / Trainees Impacted', max: 5000 },
                                { key: 'training_completed', label: 'Own Training / Upskilling Done', max: 20 },
                                { key: 'courses_developed', label: 'Courses / Modules Developed', max: 50 },
                                { key: 'income_stability', label: 'Income Stability (1-5)', max: 5 }
                            ];
                        } else if (domain === 'Business & Administration') {
                            fields = [
                                { key: 'years_experience', label: 'Years of Experience', max: 40 },
                                { key: 'team_managed', label: 'Team / Staff Managed', max: 100 },
                                { key: 'processes_improved', label: 'Processes Improved / Automated', max: 30 },
                                { key: 'training_completed', label: 'Management Trainings Done', max: 20 },
                                { key: 'income_stability', label: 'Income Stability (1-5)', max: 5 }
                            ];
                        } else if (domain === 'Creative & Media') {
                            fields = [
                                { key: 'portfolio_items', label: 'Portfolio / Published Works', max: 100 },
                                { key: 'clients_served', label: 'Clients Served', max: 200 },
                                { key: 'exhibitions_or_sales', label: 'Exhibitions / Shows / Sales', max: 50 },
                                { key: 'training_completed', label: 'Creative Workshops / Courses Done', max: 20 },
                                { key: 'income_stability', label: 'Income Stability (1-5)', max: 5 }
                            ];
                        } else if (domain === 'Service Industry') {
                            fields = [
                                { key: 'years_experience', label: 'Years of Experience', max: 30 },
                                { key: 'customers_served_monthly', label: 'Customers Served / Month', max: 3000 },
                                { key: 'training_completed', label: 'Hospitality / Service Trainings Done', max: 20 },
                                { key: 'work_output_monthly', label: 'Work Shifts / Month', max: 30 },
                                { key: 'income_stability', label: 'Income Stability (1-5)', max: 5 }
                            ];
                        } else if (domain === 'Entrepreneurship') {
                            fields = [
                                { key: 'business_years', label: 'Years Running Business', max: 30 },
                                { key: 'employees_count', label: 'People Employed', max: 100 },
                                { key: 'products_delivered_monthly', label: 'Products / Services Delivered / Month', max: 500 },
                                { key: 'training_completed', label: 'Business / Skill Trainings Done', max: 20 },
                                { key: 'income_stability', label: 'Income Stability (1-5)', max: 5 }
                            ];
                        } else {
                            fields = [
                                { key: 'years_experience', label: 'Years of Experience', max: 40 },
                                { key: 'work_output_monthly', label: 'Work Output / Month', max: 200 },
                                { key: 'training_completed', label: 'Trainings Completed', max: 20 },
                                { key: 'customers_served_monthly', label: 'People / Customers Served', max: 2000 },
                                { key: 'income_stability', label: 'Income Stability (1-5)', max: 5 }
                            ];
                        }

                        return (
                            <div className="grid grid-cols-2 gap-4">
                                {fields.map(f => (
                                    <div key={f.key}>
                                        <label className="text-xs text-gray-400 block mb-1">{f.label}</label>
                                        <input
                                            type="number"
                                            value={signals[f.key] || 0}
                                            onChange={(e) => handleChange(e, f.key)}
                                            className="w-full bg-gray-900 border border-gray-700 rounded p-2 text-sm text-white focus:border-accent outline-none font-mono"
                                            placeholder="0"
                                            min="0"
                                            max={f.max}
                                        />
                                    </div>
                                ))}
                            </div>
                        );
                    })()}
                </div>
            )
        },
        {
            id: 'proof',
            title: language === 'en' ? 'Proof of Work Verification' : 'कार्य प्रमाण सत्यापन',
            icon: Link2,
            content: (
                <div className="space-y-4">
                    <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-amber-500/10 border border-amber-500/20 mb-1">
                        <CheckCircle className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                        <span className="text-[11px] text-amber-300">Skill confidence increases with verified work evidence.</span>
                    </div>

                    {/* ── Document Uploads ── */}
                    <div>
                        <div className="text-xs font-bold text-gray-300 uppercase tracking-wider mb-3">Upload Work Evidence</div>
                        <div className="space-y-2">
                            {[
                                { key: 'work_photos', label: 'Work Photos (shop, product, service)', icon: '📸' },
                                { key: 'training_certificate', label: 'Training Certificate', icon: '📜' },
                                { key: 'upi_screenshot', label: 'UPI / Payment Transaction Screenshot', icon: '💳' },
                                { key: 'business_license', label: 'Business Document / License / ID', icon: '📋' }
                            ].map(doc => (
                                <label key={doc.key} className={`flex items-center gap-3 p-2.5 rounded-lg border cursor-pointer transition-all ${proofDocs[doc.key]
                                    ? 'bg-emerald-900/20 border-emerald-500/40'
                                    : 'bg-gray-900/50 border-gray-800 hover:border-gray-600'
                                    }`}>
                                    <input
                                        type="checkbox"
                                        checked={proofDocs[doc.key]}
                                        onChange={() => handleDocToggle(doc.key)}
                                        className="accent-emerald-500 w-4 h-4"
                                    />
                                    <span className="text-sm">{doc.icon}</span>
                                    <span className="text-xs text-gray-300">{doc.label}</span>
                                    {proofDocs[doc.key] && <CheckCircle size={14} className="text-emerald-400 ml-auto" />}
                                </label>
                            ))}
                        </div>
                    </div>

                    {/* ── Optional Business Info ── */}
                    <div className="border-t border-gray-800 pt-3">
                        <div className="text-xs font-bold text-gray-300 uppercase tracking-wider mb-3">Business / Work Details (Optional)</div>
                        <div className="grid grid-cols-2 gap-3">
                            <div>
                                <label className="text-[11px] text-gray-500 block mb-1">Monthly Customer Count</label>
                                <input
                                    type="number"
                                    value={businessInfo.monthly_customers}
                                    onChange={(e) => handleBusinessChange('monthly_customers', e.target.value)}
                                    className="w-full bg-gray-900 border border-gray-700 rounded p-2 text-sm text-white focus:border-accent outline-none font-mono"
                                    placeholder="e.g. 50"
                                    min="0"
                                />
                            </div>
                            <div>
                                <label className="text-[11px] text-gray-500 block mb-1">Income Range</label>
                                <select
                                    value={businessInfo.income_range}
                                    onChange={(e) => handleBusinessChange('income_range', e.target.value)}
                                    className="w-full bg-gray-900 border border-gray-700 rounded p-2 text-sm text-white focus:border-accent outline-none"
                                >
                                    <option value="">Select…</option>
                                    <option value="below_10k">Below ₹10,000 / month</option>
                                    <option value="10k_25k">₹10,000 – ₹25,000</option>
                                    <option value="25k_50k">₹25,000 – ₹50,000</option>
                                    <option value="50k_1L">₹50,000 – ₹1,00,000</option>
                                    <option value="above_1L">Above ₹1,00,000</option>
                                </select>
                            </div>
                            <div>
                                <label className="text-[11px] text-gray-500 block mb-1">Business / Shop Name</label>
                                <input
                                    type="text"
                                    value={businessInfo.business_name}
                                    onChange={(e) => handleBusinessChange('business_name', e.target.value)}
                                    className="w-full bg-gray-900 border border-gray-700 rounded p-2 text-sm text-white focus:border-accent outline-none"
                                    placeholder="Optional"
                                />
                            </div>
                            <div>
                                <label className="text-[11px] text-gray-500 block mb-1">Platform Presence</label>
                                <select
                                    value={businessInfo.platform_presence}
                                    onChange={(e) => handleBusinessChange('platform_presence', e.target.value)}
                                    className="w-full bg-gray-900 border border-gray-700 rounded p-2 text-sm text-white focus:border-accent outline-none"
                                >
                                    <option value="">Select…</option>
                                    <option value="none">No online presence</option>
                                    <option value="whatsapp">WhatsApp Business</option>
                                    <option value="google_business">Google Business</option>
                                    <option value="marketplace">Online Marketplace (Amazon, Flipkart, etc.)</option>
                                    <option value="multiple">Multiple platforms</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    {/* ── Verify Button ── */}
                    <button
                        onClick={verifySources}
                        disabled={verifying}
                        className="w-full bg-accent hover:bg-accent/80 text-black font-bold py-2.5 rounded flex items-center justify-center gap-2 transition-all mt-2"
                    >
                        {verifying ? <Loader2 className="animate-spin w-4 h-4" /> : <CheckCircle className="w-4 h-4" />}
                        {verifying ? 'VERIFYING...' : 'VERIFY WORK EVIDENCE'}
                    </button>

                    {/* ── Verification Results ── */}
                    {verification && (
                        <div className="mt-3 border border-gray-700 rounded-lg p-4 bg-gray-900/50 space-y-3">
                            <div className="text-xs font-bold text-gray-300 uppercase tracking-wider">Verification Results</div>

                            {/* Document statuses */}
                            {[
                                { label: 'Work Photos', key: 'work_photos' },
                                { label: 'Training Certificate', key: 'training_certificate' },
                                { label: 'UPI / Payment Proof', key: 'upi_screenshot' },
                                { label: 'Business Document', key: 'business_license' }
                            ].map((doc, i) => (
                                <div key={i} className="flex items-center justify-between text-xs">
                                    <span className="text-gray-400">{doc.label}</span>
                                    {verification.documents?.[doc.key]
                                        ? <span className="text-emerald-400 flex items-center gap-1"><CheckCircle size={12} /> Submitted</span>
                                        : <span className="text-gray-600 flex items-center gap-1"><XCircle size={12} /> Not Provided</span>
                                    }
                                </div>
                            ))}

                            {/* Score bar */}
                            <div className="border-t border-gray-700 pt-2 mt-1">
                                <div className="flex items-center justify-between text-xs mb-1">
                                    <span className="text-gray-400">Proof Strength Score</span>
                                    <span className="font-mono font-bold text-accent">{verification.proof_strength_score} / 100</span>
                                </div>
                                <div className="w-full bg-gray-800 rounded-full h-2">
                                    <div
                                        className={`h-2 rounded-full transition-all duration-700 ${verification.proof_strength_score >= 70 ? 'bg-emerald-500'
                                            : verification.proof_strength_score >= 40 ? 'bg-amber-500'
                                                : 'bg-red-500'
                                            }`}
                                        style={{ width: `${verification.proof_strength_score}%` }}
                                    ></div>
                                </div>
                            </div>

                            {/* Level badge */}
                            <div className="flex items-center justify-between text-xs border-t border-gray-700 pt-2">
                                <span className="text-gray-300 font-bold">Verification Level</span>
                                <span className={`font-bold px-3 py-1 rounded-full text-xs ${verification.verification_level === 'High' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' :
                                    verification.verification_level === 'Medium' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' :
                                        'bg-red-500/20 text-red-400 border border-red-500/30'
                                    }`}>
                                    {verification.verification_level}
                                </span>
                            </div>
                        </div>
                    )}
                </div>
            )
        }
    ];

    return (
        <div className="bg-panel border border-gray-800 rounded-lg overflow-hidden h-fit sticky top-6">
            <div className="p-3 bg-gray-900 border-b border-gray-800 flex justify-between items-center">
                <span className="font-bold text-sm text-gray-300">SIGNAL INPUT CONSOLE</span>
                <div className="flex gap-2">
                    <button
                        onClick={runDemoScenarioUrban}
                        className="text-[10px] bg-blue-500/20 hover:bg-blue-500/40 text-blue-400 px-2 py-1 rounded border border-blue-500/30 transition-colors"
                    >
                        DEMO: URBAN PRO
                    </button>
                    <button
                        onClick={runDemoScenario}
                        className="text-[10px] bg-accent/20 hover:bg-accent/40 text-accent px-2 py-1 rounded border border-accent/30 transition-colors"
                    >
                        DEMO: RURAL TALENT
                    </button>
                </div>
            </div>
            <div>
                {sections.map((section) => {
                    const Icon = section.icon;
                    const isOpen = openSection === section.id;
                    return (
                        <div key={section.id} className="border-b border-gray-800 last:border-0">
                            <button
                                onClick={() => setOpenSection(isOpen ? null : section.id)}
                                className={`w-full flex items-center justify-between p-3 text-sm font-medium transition-colors ${isOpen ? 'bg-gray-800/50 text-white' : 'text-gray-400 hover:text-white'}`}
                            >
                                <div className="flex items-center gap-2">
                                    <Icon className="w-4 h-4" />
                                    {section.title}
                                </div>
                                {isOpen ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                            </button>
                            {isOpen && (
                                <div className="p-4 bg-gray-900/30 animate-in slide-in-from-top-2 duration-200">
                                    {section.content}
                                </div>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default InputPanel;
