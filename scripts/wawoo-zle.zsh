#!/usr/bin/env zsh
# zle widget for wawoo-skills shortcuts

wawoo-delivery-lite() {
  if [[ -n "$BUFFER" ]]; then
    BUFFER="/delivery-lite $BUFFER"
    zle reset-prompt
  else
    echo "Delivery Lite: Please specify a task."
  fi
}

wawoo-research() {
  if [[ -n "$BUFFER" ]]; then
    BUFFER="/research $BUFFER"
    zle reset-prompt
  else
    echo "Research: Please specify a topic."
  fi
}

wawoo-self-review() {
  if [[ -n "$BUFFER" ]]; then
    BUFFER="/self-review $BUFFER"
    zle reset-prompt
  else
    echo "Self Review: Please specify what to review."
  fi
}

wawoo-design-review() {
  if [[ -n "$BUFFER" ]]; then
    BUFFER="/design-review $BUFFER"
    zle reset-prompt
  else
    echo "Design Review: Please specify what to review."
  fi
}

# Bind keys
zle -N wawoo-delivery-lite
zle -N wawoo-research
zle -N wawoo-self-review
zle -N wawoo-design-review

# Configure bindings (adjust as needed)
# bindkey '^D' wawoo-delivery-lite
# bindkey '^R' wawoo-research
# bindkey '^S' wawoo-self-review
# bindkey '^G' wawoo-design-review
