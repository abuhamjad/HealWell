import { Hero } from '../sections/Hero'
import { ProblemStatement } from '../sections/ProblemStatement'
import { HowItWorks } from '../sections/HowItWorks'
import { Automation } from '../sections/Automation'
import { CTA } from '../sections/CTA'

export function Home({ setPage }: { setPage: (p: 'analysis') => void }) {
  return (
    <div>
      <Hero setPage={setPage} />
      <ProblemStatement />
      <HowItWorks />
      <Automation />
      <CTA setPage={setPage} />
    </div>
  )
}
