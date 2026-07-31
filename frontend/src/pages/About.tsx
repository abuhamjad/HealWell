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
    <div className="pt-24">
      {/* Hero Section */}
      <section className="min-h-screen flex items-center py-20 relative overflow-hidden">
        <div className="max-w-6xl mx-auto px-4 w-full">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass border border-blue-400/25 text-blue-400 text-sm font-medium mb-8 w-fit">
            <span className="w-2 h-2 rounded-full bg-blue-400 animate-pulse" />
            About HealWell
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-5xl lg:text-6xl font-black leading-[1.08] mb-6"
            style={{ fontFamily: 'Manrope, sans-serif', letterSpacing: '-0.02em' }}>
            AI-Powered<br />Health Analysis<br />
            <span className="gradient-text">Platform</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="text-lg leading-relaxed mb-10 max-w-3xl"
            style={{ color: 'rgba(255,255,255,0.64)' }}>
            HealWell is an AI-powered health analysis platform that helps users better understand their symptoms through an intelligent multi-agent AI workflow. Users can describe their symptoms in natural language and receive structured health insights including risk assessment, specialist recommendations, home care guidance, lifestyle recommendations, and monitoring advice.
          </motion.p>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.35 }}
            className="text-lg leading-relaxed mb-12 max-w-3xl"
            style={{ color: 'rgba(255,255,255,0.52)' }}>
            The platform combines a modern React frontend with a FastAPI backend while LangGraph orchestrates multiple AI agents powered by Groq's OpenAI-compatible models to deliver fast, structured, and reliable health analysis.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="flex flex-col sm:flex-row gap-4">
            <a href="https://github.com" target="_blank" rel="noopener noreferrer"
              className="btn-ghost flex items-center justify-center gap-2 px-6 py-3 rounded-xl font-medium">
              <ExternalLink size={18} /> GitHub Repository
            </a>
            <a href="#" target="_blank" rel="noopener noreferrer"
              className="btn-ghost flex items-center justify-center gap-2 px-6 py-3 rounded-xl font-medium">
              <Globe size={18} /> Live Demo
            </a>
          </motion.div>
        </div>
      </section>

      {/* About the Project */}
      <section className="py-20 relative">
        <div className="max-w-6xl mx-auto px-4 w-full">
          <motion.div
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            className="glass rounded-3xl p-8 md:p-12 border border-white/08">
            <motion.h2
              variants={itemVariants}
              className="text-4xl font-bold mb-6 gradient-text"
              style={{ fontFamily: 'Manrope, sans-serif' }}>
              About the Project
            </motion.h2>
            <motion.p
              variants={itemVariants}
              className="text-lg leading-relaxed"
              style={{ color: 'rgba(255,255,255,0.72)' }}>
              HealWell is an AI-powered health analysis platform designed to demonstrate how modern AI workflows can assist users in understanding their symptoms through structured medical insights. By combining multiple specialized AI agents, the platform performs symptom interpretation, risk assessment, specialist recommendation, and personalized report generation within a scalable full-stack architecture.
            </motion.p>
          </motion.div>
        </div>
      </section>

      {/* Internship Information */}
      <section className="py-20 relative">
        <div className="max-w-6xl mx-auto px-4 w-full">
          <motion.div
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            className="glass rounded-3xl p-8 md:p-12 border border-white/08">
            <motion.div
              variants={itemVariants}
              className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-lg flex items-center justify-center"
                style={{ background: 'rgba(59, 130, 246, 0.15)', border: '1px solid rgba(59, 130, 246, 0.3)' }}>
                <GraduationCap size={20} className="text-blue-400" />
              </div>
              <h2 className="text-4xl font-bold gradient-text" style={{ fontFamily: 'Manrope, sans-serif' }}>
                AI Automation & Intelligent Solutions Internship
              </h2>
            </motion.div>
            <motion.p
              variants={itemVariants}
              className="text-lg leading-relaxed"
              style={{ color: 'rgba(255,255,255,0.72)' }}>
              This project was developed as part of the AI Automation & Intelligent Solutions Internship, demonstrating the practical application of artificial intelligence, workflow orchestration, modern backend engineering, frontend development, cloud deployment, and collaborative software development practices.
            </motion.p>
          </motion.div>
        </div>
      </section>

      {/* Technology Architecture */}
      <section className="py-20 relative">
        <div className="max-w-6xl mx-auto px-4 w-full">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true, margin: "-100px" }}
            className="mb-16">
            <h2 className="text-4xl font-bold text-center mb-12 gradient-text"
              style={{ fontFamily: 'Manrope, sans-serif' }}>
              Technology Architecture
            </h2>

            <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
              {technologies.map((tech, idx) => {
                const Icon = tech.icon
                return (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: idx * 0.1 }}
                    className="glass rounded-2xl p-8 border border-white/08 flex flex-col items-center text-center">
                    <div className="w-14 h-14 rounded-xl flex items-center justify-center mb-4"
                      style={{ background: 'rgba(59, 130, 246, 0.15)', border: '1px solid rgba(59, 130, 246, 0.3)' }}>
                      <Icon size={28} className="text-blue-400" />
                    </div>
                    <h3 className="text-xl font-bold mb-4" style={{ fontFamily: 'Manrope, sans-serif' }}>
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
      <section className="py-20 relative">
        <div className="max-w-6xl mx-auto px-4 w-full">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true, margin: "-100px" }}>
            <h2 className="text-4xl font-bold text-center mb-12 gradient-text"
              style={{ fontFamily: 'Manrope, sans-serif' }}>
              Project Highlights
            </h2>

            <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {highlights.map((highlight, idx) => {
                const Icon = highlight.icon
                return (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: idx * 0.08 }}
                    className="glass rounded-2xl p-6 border border-white/08 flex flex-col items-center text-center">
                    <div className="w-12 h-12 rounded-lg flex items-center justify-center mb-4"
                      style={{ background: 'rgba(6, 182, 212, 0.15)', border: '1px solid rgba(6, 182, 212, 0.3)' }}>
                      <Icon size={24} className="text-cyan-400" />
                    </div>
                    <h3 className="font-bold mb-2" style={{ fontFamily: 'Manrope, sans-serif' }}>
                      {highlight.label}
                    </h3>
                    <p className="text-sm" style={{ color: 'rgba(255, 255, 255, 0.52)' }}>
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
      <section className="py-20 relative">
        <div className="max-w-6xl mx-auto px-4 w-full">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true, margin: "-100px" }}>
            <h2 className="text-4xl font-bold text-center mb-12 gradient-text"
              style={{ fontFamily: 'Manrope, sans-serif' }}>
              Contributors
            </h2>

            <div className="grid md:grid-cols-2 gap-8">
              {contributors.map((contributor, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: idx * 0.1 }}
                  className="glass rounded-2xl p-8 border border-white/08">
                  <div className="flex items-center gap-4 mb-6">
                    <div className="w-14 h-14 rounded-full flex items-center justify-center flex-shrink-0"
                      style={{ background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(6, 182, 212, 0.2))' }}>
                      <UserRound size={24} className="text-blue-400" />
                    </div>
                    <div>
                      <h3 className="font-bold text-lg" style={{ fontFamily: 'Manrope, sans-serif' }}>
                        {contributor.name}
                      </h3>
                      <span className="text-xs px-2 py-1 rounded-full inline-block mt-1"
                        style={{
                          background: 'rgba(59, 130, 246, 0.15)',
                          border: '1px solid rgba(59, 130, 246, 0.3)',
                          color: '#60A5FA'
                        }}>
                        {contributor.role}
                      </span>
                    </div>
                  </div>
                  <p className="text-base leading-relaxed"
                    style={{ color: 'rgba(255, 255, 255, 0.72)' }}>
                    {contributor.description}
                  </p>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>
      </section>

      {/* Medical Disclaimer */}
      <section className="py-20 relative">
        <div className="max-w-6xl mx-auto px-4 w-full">
          <motion.div
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            className="glass rounded-3xl p-8 md:p-12 border border-orange-400/20 bg-orange-400/5">
            <motion.div
              variants={itemVariants}
              className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 mt-1"
                style={{ background: 'rgba(249, 115, 22, 0.15)', border: '1px solid rgba(249, 115, 22, 0.3)' }}>
                <TriangleAlert size={18} className="text-orange-500" />
              </div>
              <div>
                <h2 className="text-2xl font-bold mb-3" style={{ fontFamily: 'Manrope, sans-serif' }}>
                  Medical Disclaimer
                </h2>
                <p className="text-lg leading-relaxed"
                  style={{ color: 'rgba(255,255,255,0.72)' }}>
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