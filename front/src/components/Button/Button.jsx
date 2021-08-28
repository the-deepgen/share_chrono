import React from "react";
import Button from "@material-ui/core/Button";

export default function ContainedButtons({ text, onClick, disabled = false }) {
  return (
    <div>
      <Button
        variant="contained"
        color="primary"
        disabled={disabled}
        onClick={onClick}
      >
        {text}
      </Button>
    </div>
  );
}
