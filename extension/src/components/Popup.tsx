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
import SettingsIcon from '@mui/icons-material/Settings';
import { MLISRequest, MLISResponse } from "../extension/types";

function Popup() {
    const [isLoading, setIsLoading] = useState(true);
    const [content, setContent] = useState('');
    const [articleTitle, setArticleTitle] = useState('');

    useEffect(() => {
        chrome.windows.getCurrent(w => {
            chrome.tabs.query({ active: true, windowId: w.id }, ([tab]) => {
                const request: MLISRequest = {
                    url: tab.url,
                };
                chrome.runtime.sendMessage(request, (response: MLISResponse) => {
                    if (response.status == 200 && response.articleSummary) {
                        setArticleTitle(response.articleTitle!);
                        setContent(response.articleSummary!);
                        setIsLoading(false);
                    }
                    else if (response.status == 202) {
                        setContent(response.message!);
                        setIsLoading(false);
                    }
                });
            });
        });
    }, []);

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
                    {(isLoading)
                        ? <CircularProgress />
                        : (
                            <>
                                <CardContent>
                                    <Typography sx={{ fontSize: 18 }}>
                                        {articleTitle}
                                    </Typography>
                                </CardContent>
                                <CardContent>
                                    <Typography variant="body2"> {content} </Typography>
                                </CardContent>
                            </>
                        )
                    }
                </CardContent>
            </Card>
        </>
    );
};

export default Popup;
