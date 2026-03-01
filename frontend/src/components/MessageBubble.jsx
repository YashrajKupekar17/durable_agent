import React, { memo } from "react";

const MessageBubble = memo(({ message, fallback = "", isUser = false }) => {
  const displayText = message.response?.trim() ? message.response : fallback;

  if (displayText.startsWith("###")) {
    return null;
  }

  const renderTextWithLinks = (text) => {
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    const parts = text.split(urlRegex);

    return parts.map((part, index) => {
      // In renderTextWithLinks, after the urlRegex.test(part) check, clean the URL:

if (urlRegex.test(part)) {
  const cleanUrl = part.replace(/[.,!?]+$/, ""); // strip trailing punctuation
  const isPreview = cleanUrl.includes("/preview/");
  return (
    <span key={index}>
      <a
        href={cleanUrl}
        target="_blank"
        rel="noopener noreferrer"
        className="text-blue-500 hover:text-blue-600 underline"
        aria-label={`External link to ${cleanUrl}`}
      >
        {cleanUrl}
      </a>
      {isPreview && (
        <div className="mt-3 w-full">
          <iframe
            src={cleanUrl}
            className="w-full rounded-lg border border-gray-300 dark:border-gray-600 shadow-md"
            style={{ height: "420px" }}
            title="Webpage Preview"
            sandbox="allow-scripts allow-same-origin"
          />
          <p className="text-xs text-gray-400 mt-1 text-center">
            Live preview —{" "}
            <a href={cleanUrl} target="_blank" rel="noopener noreferrer" className="underline ml-1">
              open in new tab
            </a>
          </p>
        </div>
      )}
    </span>
  );
}
      return part;
    });
  };

  return (
    <div
      className={`
        inline-block px-4 py-2 mb-1 rounded-lg
        ${isUser
          ? "ml-auto bg-blue-100 dark:bg-blue-900 dark:text-white max-w-[75%]"
          : "mr-auto bg-gray-200 dark:bg-gray-700 dark:text-white w-full max-w-[90%]"
        }
        break-words transition-colors duration-200
      `}
      role="article"
      aria-label={`${isUser ? "User" : "Agent"} message`}
    >
      {renderTextWithLinks(displayText)}
    </div>
  );
});

MessageBubble.displayName = "MessageBubble";
export default MessageBubble;