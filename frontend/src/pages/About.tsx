import { motion } from 'framer-motion'
import {
  Brain, ExternalLink, Globe, GraduationCap, MonitorSmartphone,
  Server, Cloud, HeartPulse, Workflow, ShieldCheck, UserRound,
  TriangleAlert
} from 'lucide-react'

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1, delayChildren: 0.1 }
  }
}

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5, ease: [0.16, 1, 0.3, 1] } }
}

const getRoleColor = (role: string) => {
  switch (role) {
    case 'Team Lead':
      return { bg: 'rgba(59, 130, 246, 0.15)', border: 'rgba(59, 130, 246, 0.3)', text: '#60A5FA' }
    case 'Frontend & System Integration':
      return { bg: 'rgba(6, 182, 212, 0.15)', border: 'rgba(6, 182, 212, 0.3)', text: '#22D3EE' }
    case 'Documentation & Version Control':
      return { bg: 'rgba(168, 85, 247, 0.15)', border: 'rgba(168, 85, 247, 0.3)', text: '#D8B4FE' }
    case 'Quality Assurance':
      return { bg: 'rgba(34, 197, 94, 0.15)', border: 'rgba(34, 197, 94, 0.3)', text: '#86EFAC' }
    default:
      return { bg: 'rgba(59, 130, 246, 0.15)', border: 'rgba(59, 130, 246, 0.3)', text: '#60A5FA' }
  }
}

export function About() {
  const contributors = [
    {
      name: 'Abu Huraira',
      role: 'Team Lead',
      description: 'Designed the overall system architecture, developed the backend, established the application design system, implemented API integration, and oversaw project testing.'
    },
    {
      name: 'Adarsh Kumar',
      role: 'Frontend & System Integration',
      description: 'Developed the React frontend and integrated the frontend with backend services to ensure seamless communication across the application.'
    },
    {
      name: 'Abhinav Shukla',
      role: 'Documentation & Version Control',
      description: 'Prepared project documentation, maintained repository organization, and managed version control throughout the development lifecycle.'
    },
    {
      name: 'Amit Rawat',
      role: 'Quality Assurance',
      description: 'Performed quality assurance testing, validated application workflows, reported issues, and verified functionality across development milestones.'
    }
  ]

  const highlights = [
    { icon: Brain, label: 'AI-Powered Analysis', description: 'Intelligent multi-agent workflow' },
    { icon: Workflow, label: 'Multi-Agent Workflow', description: 'Specialized AI agents orchestrated' },
    { icon: Cloud, label: 'Cloud Deployment', description: 'Scalable and reliable infrastructure' },
    { icon: ShieldCheck, label: 'Modern Full-Stack', description: 'React + FastAPI + LangGraph' }
  ]

  const technologies = [
    {
      title: 'Frontend',
      icon: MonitorSmartphone,
      items: ['React', 'TypeScript', 'Vite', 'Tailwind CSS']
    },
    {
      title: 'Backend',
      icon: Server,
      items: ['Python', 'FastAPI', 'REST API']
    },
    {
      title: 'AI Engine',
      icon: Brain,
      items: ['LangGraph', 'Groq', 'GPT-OSS-120B']
    },
    {
      title: 'Deployment',
      icon: Cloud,
      items: ['Vercel', 'Render']
    }
  ]

  return (
    <div className="pt-16">
      {/* Hero Section */}
      <section className="py-10 relative overflow-hidden">
        <div className="max-w-6xl mx-auto px-4 w-full">

          <motion.h1
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-4xl lg:text-5xl font-black leading-[1.1] mb-4"
            style={{ fontFamily: 'Manrope, sans-serif', letterSpacing: '-0.02em' }}>
            AI-Powered<br />Health Analysis<br />
            <span className="gradient-text">Platform</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="text-base leading-relaxed mb-3 max-w-2xl"
            style={{ color: 'rgba(255,255,255,0.64)' }}>
            HealWell is an AI-powered health analysis platform that helps users better understand their symptoms through an intelligent multi-agent AI workflow. Users can describe their symptoms in natural language and receive structured health insights including risk assessment, specialist recommendations, home care guidance, lifestyle recommendations, and monitoring advice.
          </motion.p>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.35 }}
            className="text-base leading-relaxed mb-8 max-w-2xl"
            style={{ color: 'rgba(255,255,255,0.52)' }}>
            The platform combines a modern React frontend with a FastAPI backend while LangGraph orchestrates multiple AI agents powered by Groq's OpenAI-compatible models to deliver fast, structured, and reliable health analysis.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="flex flex-col sm:flex-row gap-4">
            <a href="https://github.com/abuhamjad/HealWell" target="_blank" rel="noopener noreferrer"
              className="btn-ghost flex items-center justify-center gap-2 px-6 py-3 rounded-xl font-medium">
              <ExternalLink size={18} /> GitHub Repository
            </a>
            <a href="https://heal-well-three.vercel.app/" target="_blank" rel="noopener noreferrer"
              className="btn-ghost flex items-center justify-center gap-2 px-6 py-3 rounded-xl font-medium">
              <Globe size={18} /> Live Demo
            </a>
          </motion.div>
        </div>
      </section>

      {/* About the Project */}
      <section className="py-10 relative">
        <div className="max-w-6xl mx-auto px-4 w-full">
          <motion.div
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            className="glass rounded-3xl p-6 md:p-8 border border-white/08">
            <motion.h2
              variants={itemVariants}
              className="text-2xl font-bold mb-4 gradient-text"
              style={{ fontFamily: 'Manrope, sans-serif' }}>
              About the Project
            </motion.h2>
            <motion.p
              variants={itemVariants}
              className="text-base leading-relaxed"
              style={{ color: 'rgba(255,255,255,0.72)' }}>
              HealWell is an AI-powered healthcare platform that uses a multi-agent AI workflow to provide symptom analysis, health risk assessment, specialist recommendations, and personalized health insights, making healthcare information more accessible and informative.
            </motion.p>
          </motion.div>
        </div>
      </section>

      {/* Internship Information */}
      <section className="py-12 relative">
        <div className="max-w-6xl mx-auto px-4 w-full">
          <motion.div
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            className="glass rounded-3xl p-6 md:p-8 border border-white/08">
            <motion.div
              variants={itemVariants}
              className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0"
                style={{ background: 'rgba(59, 130, 246, 0.15)', border: '1px solid rgba(59, 130, 246, 0.3)' }}>
                <GraduationCap size={20} className="text-blue-400" />
              </div>
              <h2 className="text-2xl font-bold gradient-text" style={{ fontFamily: 'Manrope, sans-serif' }}>
                IBM SkillsBuild Internship
              </h2>
            </motion.div>
            <motion.p
              variants={itemVariants}
              className="text-base leading-relaxed"
              style={{ color: 'rgba(255,255,255,0.72)' }}>
              This project was developed as part of the IBM SkillsBuild AI Automation & Intelligent Solutions Internship, addressing UN Sustainable Development Goal 3 (Good Health & Well-being) through an AI-powered healthcare assistance platform.
            </motion.p>
          </motion.div>
        </div>
      </section>

      {/* Technology Architecture */}
      <section className="py-12 relative">
        <div className="max-w-6xl mx-auto px-4 w-full">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true, margin: "-100px" }}
            className="mb-8">
            <h2 className="text-3xl font-bold text-center mb-8 gradient-text"
              style={{ fontFamily: 'Manrope, sans-serif' }}>
              Technology Stack
            </h2>

            <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
              {technologies.map((tech, idx) => {
                const Icon = tech.icon
                return (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: idx * 0.1 }}
                    className="glass rounded-2xl p-5 border border-white/08 flex flex-col items-center text-center">
                    <div className="w-12 h-12 rounded-lg flex items-center justify-center mb-3"
                      style={{ background: 'rgba(59, 130, 246, 0.15)', border: '1px solid rgba(59, 130, 246, 0.3)' }}>
                      <Icon size={24} className="text-blue-400" />
                    </div>
                    <h3 className="text-lg font-bold mb-3" style={{ fontFamily: 'Manrope, sans-serif' }}>
                      {tech.title}
                    </h3>
                    <div className="flex flex-wrap gap-2 justify-center">
                      {tech.items.map((item, i) => (
                        <span
                          key={i}
                          className="text-sm px-3 py-1.5 rounded-full"
                          style={{
                            background: 'rgba(255, 255, 255, 0.05)',
                            border: '1px solid rgba(255, 255, 255, 0.1)',
                            color: 'rgba(255, 255, 255, 0.72)'
                          }}>
                          {item}
                        </span>
                      ))}
                    </div>
                  </motion.div>
                )
              })}
            </div>
          </motion.div>
        </div>
      </section>

      {/* Project Highlights */}
      <section className="py-12 relative">
        <div className="max-w-6xl mx-auto px-4 w-full">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true, margin: "-100px" }}>
            <h2 className="text-3xl font-bold text-center mb-8 gradient-text"
              style={{ fontFamily: 'Manrope, sans-serif' }}>
              Project Highlights
            </h2>

            <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
              {highlights.map((highlight, idx) => {
                const Icon = highlight.icon
                return (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: idx * 0.08 }}
                    className="glass rounded-2xl p-5 border border-white/08 flex flex-col items-center text-center">
                    <div className="w-10 h-10 rounded-lg flex items-center justify-center mb-3"
                      style={{ background: 'rgba(6, 182, 212, 0.15)', border: '1px solid rgba(6, 182, 212, 0.3)' }}>
                      <Icon size={20} className="text-cyan-400" />
                    </div>
                    <h3 className="text-sm font-bold mb-2" style={{ fontFamily: 'Manrope, sans-serif' }}>
                      {highlight.label}
                    </h3>
                    <p className="text-xs" style={{ color: 'rgba(255, 255, 255, 0.52)' }}>
                      {highlight.description}
                    </p>
                  </motion.div>
                )
              })}
            </div>
          </motion.div>
        </div>
      </section>

      {/* Contributors */}
      <section className="py-12 relative">
        <div className="max-w-6xl mx-auto px-4 w-full">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true, margin: "-100px" }}>
            <h2 className="text-3xl font-bold text-center mb-8 gradient-text"
              style={{ fontFamily: 'Manrope, sans-serif' }}>
              Contributors
            </h2>

            <div className="grid md:grid-cols-2 gap-6">
              {contributors.map((contributor, idx) => {
                const roleColor = getRoleColor(contributor.role)
                return (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: idx * 0.1 }}
                    className="glass rounded-2xl p-6 border border-white/08">
                    <div className="flex items-center gap-3 mb-4">
                      <div className="w-12 h-12 rounded-full flex items-center justify-center shrink-0"
                        style={{ background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(6, 182, 212, 0.2))' }}>
                        <UserRound size={20} className="text-blue-400" />
                      </div>
                      <div>
                        <h3 className="font-bold text-base" style={{ fontFamily: 'Manrope, sans-serif' }}>
                          {contributor.name}
                        </h3>
                        <span className="text-xs px-2 py-0.5 rounded-full inline-block mt-0.5"
                          style={{
                            background: roleColor.bg,
                            border: `1px solid ${roleColor.border}`,
                            color: roleColor.text
                          }}>
                          {contributor.role}
                        </span>
                      </div>
                    </div>
                    <p className="text-sm leading-relaxed"
                      style={{ color: 'rgba(255, 255, 255, 0.72)' }}>
                      {contributor.description}
                    </p>
                  </motion.div>
                )
              })}
            </div>
          </motion.div>
        </div>
      </section>

      {/* Medical Disclaimer */}
      <section className="py-12 relative">
        <div className="max-w-6xl mx-auto px-4 w-full">
          <motion.div
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            className="rounded-3xl p-6 md:p-8 border border-amber-600/25"
            style={{ background: 'rgba(180, 83, 9, 0.08)' }}>
            <motion.div
              variants={itemVariants}
              className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-lg flex items-center justify-center shrink-0 mt-0.5"
                style={{ background: 'rgba(251, 146, 60, 0.15)', border: '1px solid rgba(251, 146, 60, 0.3)' }}>
                <TriangleAlert size={16} className="text-orange-400" />
              </div>
              <div>
                <h2 className="text-xl font-bold mb-2" style={{ fontFamily: 'Manrope, sans-serif' }}>
                  Medical Disclaimer
                </h2>
                <p className="text-sm leading-relaxed"
                  style={{ color: 'rgba(255,255,255,0.68)' }}>
                  HealWell provides AI-generated health information for educational and informational purposes only. It is not intended to replace professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional regarding any medical concerns.
                </p>
              </div>
            </motion.div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}