import { useState } from 'react'
import { motion } from 'framer-motion'
import { User, FileText, Heart, Users, Save, AlertCircle } from 'lucide-react'

export function Profile() {
  const [formData, setFormData] = useState({
    fullName: '',
    preferredName: '',
    dateOfBirth: '',
    gender: 'male',
    height: '',
    weight: '',
    allergies: '',
    conditions: '',
    medications: '',
    medicalHistory: '',
  })

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  return (
    <div className="min-h-screen pt-28 pb-20">
      <div className="max-w-6xl mx-auto px-4">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <div className="text-center mb-12">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass border border-blue-400/25 text-blue-400 text-sm font-medium mb-6">
              <User size={14} /> Profile
            </div>
            <h1 className="text-4xl font-bold mb-4" style={{ fontFamily: 'Manrope, sans-serif' }}>
              Your Health <span className="gradient-text">Profile</span>
            </h1>
            <p className="max-w-lg mx-auto text-sm leading-relaxed" style={{ color: 'rgba(255,255,255,0.48)' }}>
              Manage your personal and medical information. This information helps us provide better health analysis.
            </p>
          </div>

          <div className="grid lg:grid-cols-2 gap-6">
            {/* Patient Information */}
            <div className="glass rounded-2xl p-6">
              <div className="flex items-center gap-2 mb-6">
                <User size={16} className="text-blue-400" />
                <span className="font-semibold text-base" style={{ color: 'rgba(255,255,255,0.75)' }}>
                  Patient Information
                </span>
              </div>
              <div className="space-y-4">
                {[
                  { name: 'fullName', label: 'Full Name', placeholder: 'John Doe', type: 'text' },
                  { name: 'preferredName', label: 'Preferred Name', placeholder: 'John', type: 'text' },
                  { name: 'dateOfBirth', label: 'Date of Birth', placeholder: 'MM/DD/YYYY', type: 'text' },
                  { name: 'height', label: 'Height (cm)', placeholder: '175', type: 'number' },
                  { name: 'weight', label: 'Weight (kg)', placeholder: '72', type: 'number' },
                ].map(field => (
                  <div key={field.name}>
                    <label className="text-xs font-medium mb-2 block" style={{ color: 'rgba(255,255,255,0.35)' }}>
                      {field.label}
                    </label>
                    <input
                      type={field.type}
                      name={field.name}
                      placeholder={field.placeholder}
                      value={(formData as any)[field.name]}
                      onChange={handleInputChange}
                      className="w-full glass rounded-xl px-3 py-2.5 text-sm text-white placeholder-white/20 outline-none border border-white/08 focus:border-blue-400/40 bg-transparent transition-smooth"
                    />
                  </div>
                ))}
                <div>
                  <label className="text-xs font-medium mb-2 block" style={{ color: 'rgba(255,255,255,0.35)' }}>
                    Gender
                  </label>
                  <select
                    name="gender"
                    value={formData.gender}
                    onChange={handleInputChange}
                    className="w-full glass rounded-xl px-3 py-2.5 text-sm text-white bg-[#0B0B0B] outline-none border border-white/08 focus:border-blue-400/40 transition-smooth"
                  >
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Medical History */}
            <div className="glass rounded-2xl p-6">
              <div className="flex items-center gap-2 mb-6">
                <FileText size={16} className="text-purple-400" />
                <span className="font-semibold text-base" style={{ color: 'rgba(255,255,255,0.75)' }}>
                  Medical History
                </span>
              </div>
              <div className="space-y-4">
                {[
                  { name: 'allergies', label: 'Allergies', placeholder: 'Penicillin, Latex...' },
                  { name: 'conditions', label: 'Existing Conditions', placeholder: 'Diabetes, Hypertension...' },
                  { name: 'medications', label: 'Current Medications', placeholder: 'Metformin 500mg...' },
                ].map(field => (
                  <div key={field.name}>
                    <label className="text-xs font-medium mb-2 block" style={{ color: 'rgba(255,255,255,0.35)' }}>
                      {field.label}
                    </label>
                    <input
                      type="text"
                      name={field.name}
                      placeholder={field.placeholder}
                      value={(formData as any)[field.name]}
                      onChange={handleInputChange}
                      className="w-full glass rounded-xl px-3 py-2.5 text-sm text-white placeholder-white/20 outline-none border border-white/08 focus:border-purple-400/40 bg-transparent transition-smooth"
                    />
                  </div>
                ))}
                <div>
                  <label className="text-xs font-medium mb-2 block" style={{ color: 'rgba(255,255,255,0.35)' }}>
                    Medical History Notes
                  </label>
                  <textarea
                    name="medicalHistory"
                    placeholder="Any additional medical history or notes..."
                    value={formData.medicalHistory}
                    onChange={handleInputChange}
                    className="w-full glass rounded-xl px-3 py-2.5 text-sm text-white placeholder-white/20 outline-none border border-white/08 focus:border-purple-400/40 bg-transparent transition-smooth resize-none min-h-[100px]"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Placeholder Sections */}
          <div className="grid lg:grid-cols-2 gap-6 mt-6">
            <div className="glass rounded-2xl p-6">
              <div className="flex items-center gap-2 mb-6">
                <Heart size={16} className="text-pink-400" />
                <span className="font-semibold text-base" style={{ color: 'rgba(255,255,255,0.75)' }}>
                  Lifestyle
                </span>
              </div>
              <div className="flex items-center justify-center py-16 text-center">
                <p style={{ color: 'rgba(255,255,255,0.28)' }} className="text-sm">
                  Coming soon: Lifestyle and wellness information
                </p>
              </div>
            </div>

            <div className="glass rounded-2xl p-6">
              <div className="flex items-center gap-2 mb-6">
                <Users size={16} className="text-emerald-400" />
                <span className="font-semibold text-base" style={{ color: 'rgba(255,255,255,0.75)' }}>
                  Emergency Contacts
                </span>
              </div>
              <div className="flex items-center justify-center py-16 text-center">
                <p style={{ color: 'rgba(255,255,255,0.28)' }} className="text-sm">
                  Coming soon: Add and manage emergency contacts
                </p>
              </div>
            </div>
          </div>

          {/* Info Box */}
          <div className="glass rounded-xl p-4 mt-8 flex items-start gap-3 max-w-2xl">
            <AlertCircle size={14} className="text-yellow-400 mt-0.5 flex-shrink-0" />
            <p className="text-xs leading-relaxed" style={{ color: 'rgba(255,255,255,0.38)' }}>
              <span className="text-yellow-400 font-medium">Note:</span> Your profile information is stored locally in this preview.
              Once authentication is implemented, your data will be securely saved to our servers. Always keep your medical information up to date for accurate health analysis.
            </p>
          </div>

          {/* Save Button */}
          <div className="flex justify-center mt-8">
            <button
              disabled
              className="flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-blue-500/40 to-cyan-500/40 text-white font-semibold opacity-50 cursor-not-allowed transition-smooth"
            >
              <Save size={16} /> Save Profile
            </button>
          </div>
        </motion.div>
      </div>
    </div>
  )
}
