import { cn } from "../lib/utils" // update the path if needed
import { Users, Zap } from "lucide-react"

export function RoleCard({ role, selected, onSelect }) {
  const isCreator = role === "creator"

  return (
    <div
      onClick={onSelect}
      className={cn(
        "relative cursor-pointer rounded-xl border-2 p-6 transition-all duration-300 hover:scale-[1.02]",
        selected
          ? "border-primary bg-gradient-card shadow-glow"
          : "border-border bg-card hover:border-muted-foreground"
      )}
    >
      <div className="flex items-center gap-4">
        <div
          className={cn(
            "flex h-12 w-12 items-center justify-center rounded-lg transition-all duration-300",
            selected
              ? isCreator
                ? "bg-gradient-secondary shadow-medium"
                : "bg-gradient-accent shadow-accent"
              : "bg-muted"
          )}
        >
          {isCreator ? (
            <Zap
              className={cn(
                "h-6 w-6",
                selected ? "text-secondary-foreground" : "text-muted-foreground"
              )}
            />
          ) : (
            <Users
              className={cn(
                "h-6 w-6",
                selected ? "text-accent-foreground" : "text-muted-foreground"
              )}
            />
          )}
        </div>
        <div className="flex-1">
          <h3
            className={cn(
              "font-semibold capitalize",
              selected ? "text-foreground" : "text-muted-foreground"
            )}
          >
            {role}
          </h3>
          <p className="text-sm text-muted-foreground">
            {isCreator ? "Launch and manage campaigns" : "Support amazing projects"}
          </p>
        </div>
      </div>

      {selected && (
        <div className="absolute -inset-px rounded-xl bg-gradient-primary opacity-20 blur-sm" />
      )}
    </div>
  )
}
