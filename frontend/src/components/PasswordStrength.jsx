import { cn } from "../lib/utils.js" // update the path if needed
import { Check } from "lucide-react"

export function PasswordStrength({ password }) {
  const checks = [
    { label: "At least 8 characters", valid: password.length >= 8 },
    { label: "Contains uppercase letter", valid: /[A-Z]/.test(password) },
    { label: "Contains lowercase letter", valid: /[a-z]/.test(password) },
    { label: "Contains number", valid: /\d/.test(password) },
  ]

  const validChecks = checks.filter(check => check.valid).length
  const strength = validChecks / checks.length

  return (
    <div className="mt-3 space-y-2">
      <div className="flex items-center gap-2">
        <span className="text-xs text-muted-foreground">Password strength:</span>
        <div className="flex-1 h-1.5 bg-muted rounded-full overflow-hidden">
          <div
            className={cn(
              "h-full transition-all duration-300",
              strength < 0.5 ? "bg-destructive" : strength < 0.8 ? "bg-warning" : "bg-success"
            )}
            style={{ width: `${strength * 100}%` }}
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-1">
        {checks.map((check, index) => (
          <div key={index} className="flex items-center gap-1.5 text-xs">
            <Check
              className={cn(
                "h-3 w-3",
                check.valid ? "text-success" : "text-muted-foreground"
              )}
            />
            <span className={cn(check.valid ? "text-success" : "text-muted-foreground")}>
              {check.label}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}
