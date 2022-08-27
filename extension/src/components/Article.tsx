import React, { useEffect, useState } from "react";

import {
  AppBar,
  Card,
  CardContent,
  CircularProgress,
  CssBaseline,
  Toolbar,
  Typography
} from '@mui/material';

interface ArticleProps {
  articleTitle: string,
  articleSummary: string,
  articleAuthors?: string[],
  articleDate?: Date,
}

const Article = (props: ArticleProps) => {
  const { articleTitle, articleSummary, articleAuthors, articleDate } = props

  return (
    <div>
      <CardContent>
        <Typography variant="h6"> {articleTitle} </Typography>
      </CardContent>
      <CardContent>
        <Typography variant="subtitle1"> {articleDate.toLocaleDateString()} </Typography>
      </CardContent>
      <CardContent>
        <Typography variant="subtitle1"> {articleAuthors.join(', ')} </Typography>
      </CardContent>
      <CardContent>
        <Typography variant="body2"> {articleSummary} </Typography>
      </CardContent>
    </div>
  )
}

export default Article;
