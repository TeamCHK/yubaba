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
import Article from "./Article";
import SettingsIcon from '@mui/icons-material/Settings';
import { MLISRequest, MLISResponse } from "../extension/types";

function Popup() {
    const [isLoading, setIsLoading] = useState(true);
    const [articleTitle, setArticleTitle] = useState('');
    const [articleSummary, setArticleSummary] = useState('');
    const [articleAuthors, setArticleAuthors] = useState([]);
    const [articleDate, setArticleDate] = useState(null);

    useEffect(() => {
        chrome.windows.getCurrent(w => {
            chrome.tabs.query({ active: true, windowId: w.id }, ([tab]) => {
                const request: MLISRequest = {
                    url: tab.url,
                };
                chrome.runtime.sendMessage(request, (response: MLISResponse) => {
                    if (response.status == 200 && response.articleSummary) {
                        setArticleTitle(response.articleTitle!);
                        setArticleSummary(response.articleSummary!);
                        setArticleAuthors(response.articleAuthors!);
                        setArticleDate(new Date(response.publishDate!));
                        setIsLoading(false);
                    }
                    else if (response.status == 202) {
                        setArticleTitle(response.message!);
                        setIsLoading(false);
                    }
                });
            });
        });
    }, []);

    const articleProps = { articleTitle, articleSummary, articleAuthors, articleDate }

    return (
        <>
            <CssBaseline />
            <AppBar position="static">
                <Toolbar>
                    <Typography variant="h6" color="common.white" component="div" sx={{ flexGrow: 1 }}>
                        yubaba
                    </Typography>
                    <SettingsIcon />
                </Toolbar>
            </AppBar>
            <Card sx={{ height: 400 }}>
                <CardContent>
                    {isLoading ? <CircularProgress /> : <Article {...articleProps} />}
                </CardContent>
            </Card>
        </>
    );
};

export default Popup;
